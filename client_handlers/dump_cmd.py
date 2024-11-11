import os

from client_handlers.base import *
from database.models import BotUsers
from filters import is_admin_filter


class Dump(BaseHandler):
    FILTER = command("dump") & is_admin_filter

    async def func(self):
        with open("dump.txt", "w") as f:
            db_users = BotUsers.select()
            f.write(f"Всего пользователей: {len(db_users)}")
            f.write("\n".join(map(lambda x: str(x.tg_id), db_users)))

        await self.request.reply_document(document=open("dump.txt", "rb"))

        os.remove("dump.txt")
