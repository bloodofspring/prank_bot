import os

from base import *
from database.models import BotUsers
from filters import is_admin_filter


class Dump(BaseHandler):
    FILTER = command("dump") & is_admin_filter

    async def func(self):
        with open("dump.txt", "w") as f:
            f.write("\n".join(map(lambda x: x.tg_id, BotUsers.select())))

        await self.request.reply_document(document=open("dump.txt", "rb"))

        os.remove("dump.txt")
