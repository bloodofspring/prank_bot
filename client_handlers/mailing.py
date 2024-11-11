import asyncio

from colorama import Fore

from client_handlers.base import *
from config import ADMINS
from database.models import BotUsers
from filters import is_admin_filter
from util import color_log


class Mailing(BaseHandler):
    FILTER = command("mailing") & is_admin_filter

    async def mailing(self) -> int:
        messages_sent = 0

        for user in BotUsers.select():
            sent_failed = False
            try:
                if user.tg_id in ADMINS:
                    continue

                await self.request.reply_to_message.copy(chat_id=user.tg_id)
                messages_sent += 1
                await asyncio.sleep(1)
            except:
                sent_failed = True

            print(color_log((
                f"Отправка сообщения пользователю {user.tg_id}...|success="
                f"{Fore.LIGHTCYAN_EX + 'true' if not sent_failed else Fore.LIGHTRED_EX + 'false'}"
            ),
                Fore.LIGHTWHITE_EX
            ))

        return messages_sent

    async def func(self):
        if not self.request.reply_to_message:
            await self.request.reply("Команда должна быть использована реплаем!")

            return

        print(color_log(
            f"Рассылка начинается! Ожидаемая длительность: {len(BotUsers.select())} сек", Fore.LIGHTGREEN_EX
        ))
        await self.request.reply(f"Рассылка начинается! Ожидаемая длительность: {len(BotUsers.select())} сек")
        messages_sent = await self.mailing()
        await self.request.reply(f"Рассылка завершена! Отправлено сообщений: {messages_sent}")
