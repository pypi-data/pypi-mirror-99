from io import BytesIO
import json
import logging
import os
import re
import tempfile
import shutil
import time

from jinja2 import Template
from PIL import Image
from telethon.sync import TelegramClient
import telethon.tl.types

from .db import User, Message, Media


class Sync:
    """
    Sync iterates and receives messages from the Telegram group to the
    local SQLite DB.
    """
    config = {}
    db = None

    def __init__(self, config, session_file, db):
        self.config = config
        self.db = db

        self.client = TelegramClient(
            session_file, self.config["api_id"], self.config["api_hash"])
        self.client.start()

        if not os.path.exists(self.config["media_dir"]):
            os.mkdir(self.config["media_dir"])

    def sync(self, ids=None):
        """
        Sync syncs messages from Telegram from the last synced message
        into the local SQLite DB.
        """

        if ids:
            last_id, last_date = (ids, None)
        else:
            last_id, last_date = self.db.get_last_message_id()

        if ids:
            logging.info("fetching message id={}".format(ids))
        elif last_id:
            logging.info("fetching from last message id={} ({})".format(
                last_id, last_date))

        n = 0
        while True:
            has = False
            for m in self._get_messages(self.config["group"],
                    offset_id=last_id if last_id else 0,
                    ids=ids):
                if not m:
                    continue

                has = True

                # Inser the records into DB.
                self.db.insert_user(m.user)

                if m.media:
                    self.db.insert_media(m.media)

                self.db.insert_message(m)

                last_date = m.date
                n += 1
                if n % 300 == 0:
                    logging.info("fetched {} messages".format(n))
                    self.db.commit()

                if self.config["fetch_limit"] > 0 and n >= self.config["fetch_limit"] or ids:
                    has = False
                    break

            self.db.commit()
            if has:
                last_id = m.id
                logging.info("fetched {} messages. sleeping for {} seconds".format(
                    n, self.config["fetch_wait"]))
                time.sleep(self.config["fetch_wait"])
            else:
                break

        self.db.commit()
        logging.info(
            "finished. fetched {} messages. last message = {}".format(n, last_date))

    def _get_messages(self, group, offset_id, ids=None) -> Message:
        # https://docs.telethon.dev/en/latest/quick-references/objects-reference.html#message
        for m in self.client.get_messages(group, offset_id=offset_id,
                                          limit=self.config["fetch_batch_size"],
                                          ids=ids,
                                          reverse=True):

            if not m or not m.sender:
                continue

            # Media.
            sticker = None
            med = None
            if m.media:
                # If it's a sticker, get the alt value (unicode emoji).
                if isinstance(m.media, telethon.tl.types.MessageMediaDocument) and \
                        m.media.document.mime_type == "application/x-tgsticker":
                    alt = [a.alt for a in m.media.document.attributes if isinstance(
                        a, telethon.tl.types.DocumentAttributeSticker)]
                    if len(alt) > 0:
                        sticker = alt[0]
                elif isinstance(m.media, telethon.tl.types.MessageMediaPoll):
                    med = self._make_poll(m)
                else:
                    med = self._get_media(m)

            # Message.
            typ = "message"
            if m.action:
                if isinstance(m.action, telethon.tl.types.MessageActionChatAddUser):
                    typ = "user_joined"
                elif isinstance(m.action, telethon.tl.types.MessageActionChatDeleteUser):
                    typ = "user_left"

            yield Message(
                type=typ,
                id=m.id,
                date=m.date,
                edit_date=m.edit_date,
                content=sticker if sticker else m.raw_text,
                reply_to=m.reply_to_msg_id if m.reply_to and m.reply_to.reply_to_msg_id else None,
                user=self._get_user(m.sender),
                media=med
            )

    def _get_user(self, u) -> User:
        tags = []
        is_normal_user = isinstance(u, telethon.tl.types.User)

        if is_normal_user:
            if u.bot:
                tags.append("bot")

        if u.scam:
            tags.append("scam")

        if u.fake:
            tags.append("fake")

        # Download sender's profile photo if it's not already cached.
        avatar = None
        if self.config["download_avatars"]:
            try:
                fname = self._download_avatar(u)
                avatar = fname
            except Exception as e:
                logging.error(
                    "error downloading avatar: #{}: {}".format(u.id, e))

        return User(
            id=u.id,
            username=u.username if u.username else str(u.id),
            first_name=u.first_name if is_normal_user else None,
            last_name=u.last_name if is_normal_user else None,
            tags=tags,
            avatar=avatar
        )

    def _make_poll(self, msg):
        options = [{"label": a.text, "count": 0, "correct": False}
                   for a in msg.media.poll.answers]

        total = msg.media.results.total_voters
        for i, r in enumerate(msg.media.results.results):
            options[i]["count"] = r.voters
            options[i]["percent"] = r.voters / total * 100 if total > 0 else 0
            options[i]["correct"] = r.correct

        return Media(
            id=msg.id,
            type="poll",
            url=None,
            title=msg.media.poll.question,
            description=json.dumps(options),
            thumb=None
        )

    def _get_media(self, msg):
        if isinstance(msg.media, telethon.tl.types.MessageMediaWebPage) and \
                not isinstance(msg.media.webpage, telethon.tl.types.WebPageEmpty):
            return Media(
                id=msg.id,
                type="webpage",
                url=msg.media.webpage.url,
                title=msg.media.webpage.title,
                description=msg.media.webpage.description if msg.media.webpage.description else None,
                thumb=None
            )
        elif isinstance(msg.media, telethon.tl.types.MessageMediaPhoto) or \
                isinstance(msg.media, telethon.tl.types.MessageMediaDocument) or \
                isinstance(msg.media, telethon.tl.types.MessageMediaContact):
            if self.config["download_media"]:
                logging.info("downloading media #{}".format(msg.id))
                try:
                    basename, fname, thumb = self._download_media(msg)
                    return Media(
                        id=msg.id,
                        type="photo",
                        url=fname,
                        title=basename,
                        description=None,
                        thumb=thumb
                    )
                except Exception as e:
                    logging.error(
                        "error downloading media: #{}: {}".format(msg.id, e))

    def _download_media(self, msg) -> [str, str, str]:
        """
        Download a media / file attached to a message and return its original
        filename, sanitized name on disk, and the thumbnail (if any). 
        """
        # Download the media to the temp dir and copy it back as
        # there does not seem to be a way to get the canonical
        # filename before the download.
        fpath = self.client.download_media(msg, file=tempfile.gettempdir())
        basename = os.path.basename(fpath)

        newname = "{}.{}".format(msg.id, self._get_file_ext(basename))
        shutil.move(fpath, os.path.join(self.config["media_dir"], newname))

        # If it's a photo, download the thumbnail.
        tname = None
        if isinstance(msg.media, telethon.tl.types.MessageMediaPhoto):
            tpath = self.client.download_media(
                msg, file=tempfile.gettempdir(), thumb=1)
            tname = "thumb_{}.{}".format(
                msg.id, self._get_file_ext(os.path.basename(tpath)))
            shutil.move(tpath, os.path.join(self.config["media_dir"], tname))

        return basename, newname, tname

    def _get_file_ext(self, f) -> str:
        if "." in f:
            e = f.split(".")[-1]
            if len(e) < 6:
                return e

        return ".file"

    def _download_avatar(self, user):
        fname = "avatar_{}.jpg".format(user.id)
        fpath = os.path.join(self.config["media_dir"], fname)

        if os.path.exists(fpath):
            return fname

        logging.info("downloading avatar #{}".format(user.id))

        # Download the file into a container, resize it, and then write to disk.
        b = BytesIO()
        self.client.download_profile_photo(user, file=b)

        im = Image.open(b)
        im.thumbnail(self.config["avatar_size"], Image.ANTIALIAS)
        im.save(fpath, "JPEG")

        return fname
