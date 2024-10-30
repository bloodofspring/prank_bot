from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from client_handlers.access_config import ChannelsToSub
from client_handlers.base import *


class StartCmd(BaseHandler):
    FILTER = command("start")

    @property
    async def channels_for_sub(self) -> InlineKeyboardMarkup | None:
        sub_instances = []

        for chan in ChannelsToSub.select():
            if await self.client.get_chat_member(chat_id=chan.tg_id, user_id=self.request.from_user.id):
                continue

            sub_instances.append((chan, await self.client.get_chat(chan.tg_id)))

        if not sub_instances:
            return None

        return InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text=f"Канал {sub_instances.index(c) + 1}", url=await c[0].export_invite_link())
        ] for c in sub_instances])

    async def func(self):
        keyboard = self.channels_for_sub
        if keyboard is not None:
            await self.request.reply(
                "Чтобы получить доступ к функциям бота, **необходимо подписаться на ресурсы**:",
                reply_markup=keyboard, disable_web_page_preview=True
            )
            await self.request.reply((
                f"**Привет, {self.request.from_user.first_name}**\n"
                "Чтобы пользоваться ботом, подпишись выполни задания.\n"
                "Потом, нажми на / start еще раз, чтобы получить свою ссылку."
            ))

            return

        await self.request.reply((
            "**Привет**,\n"
            "🔗 Вот твоя ссылка:\n"
            "https://deletelife.ru/vbRU3Dzp2E\n"
            "Отправляй ссылку друзьям, чтобы напугать их."
        ))
