import asyncio

from client_handlers.base import *
from config import ADMINS
from database.models import BotUsers
from filters import is_admin


class Mailing(BaseHandler):
    FILTER = command("mailing") & is_admin

    async def mailing(self) -> int:
        messages_sent = 0

        for user in BotUsers.select():
            try:
                if user.tg_id in ADMINS:
                    continue

                await self.request.reply_to_message.copy(chat_id=user.tg_id)
                messages_sent += 1
                await asyncio.sleep(1)
            except:
                pass

        return messages_sent

    async def func(self):
        if not self.request.reply_to_message:
            await self.request.reply("Команда должна быть использована реплаем!")

            return

        await self.request.reply(f"Рассылка начинается! Ожидаемая длительность: {len(BotUsers.select())} сек")
        messages_sent = await self.mailing()
        await self.request.reply(f"Рассылка завершена! Отправлено сообщений: {messages_sent}")
