import os

from client_handlers.base import *
from database.models import BotUsers
from filters import is_admin_filter


class Dump(BaseHandler):
    FILTER = command("dump") & is_admin_filter

    async def func(self):
        with open("dump.txt", "w") as f:
            db_users = BotUsers.select()
            subscribed = len(BotUsers.select().where(BotUsers.is_subscribed_to_op))
            all_ = len(BotUsers.select())
            percent = '{:.2f}%'.format(round((subscribed / all_) * 100, 2))
            f.write(f"Всего пользователей: {len(db_users)}\n")
            f.write(f"Подписанных на ОП пользователей: {subscribed}/{all_} ({percent})\n")
            f.write("\n".join(map(lambda x: str(x.telegram_id), db_users)))

        await self.request.reply_document(document=open("dump.txt", "rb"))

        os.remove("dump.txt")
