import asyncio

from pyrogram.types import Message

from client_handlers.base import *
from config import OP_USERS
from database.models import BotUsers


def is_admin(_, __, m: Message):
    return m and m.from_user and m.from_user.id in OP_USERS


is_admin_filter = create(is_admin)


class Mailing(BaseHandler):
    FILTER = command("mailing") & is_admin_filter

    async def mailing(self) -> int:
        messages_sent = 0

        for user in BotUsers.select():
            try:
                if user.tg_id in OP_USERS:
                    continue

                await self.request.reply_to_message.copy(chat_id=user.tg_id)
                messages_sent += 1
                await asyncio.sleep(1)  # Чтобы клиента не забанили
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
