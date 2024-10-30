from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from client_handlers.base import *
from config import OP_USERS
from database.models import ChannelsToSub


class StartCmd(BaseHandler):
    FILTER = command("start")

    @property
    async def channels_for_sub(self) -> InlineKeyboardMarkup | None:
        sub_instances = []

        for chan in ChannelsToSub.select():
            try:
                await self.client.get_chat_member(chat_id=chan.tg_id, user_id=self.request.from_user.id)
            except:
                sub_instances.append(chan)

        if not sub_instances:
            return None

        return InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text=f"Канал {sub_instances.index(c) + 1}", url=f"https://t.me/{c.tg_id.strip('@')}")
        ] for c in sub_instances])

    async def func(self):
        keyboard = await self.channels_for_sub
        if keyboard is not None and self.request.from_user.id not in OP_USERS:
            await self.request.reply(
                "Чтобы получить доступ к функциям бота, **необходимо подписаться на ресурсы**:",
                reply_markup=keyboard, disable_web_page_preview=True
            )
            await self.request.reply((
                f"**Привет, {self.request.from_user.first_name}**\n"
                "Чтобы пользоваться ботом, подпишись выполни задания.\n"
                "Потом, нажми на /start еще раз, чтобы получить свою ссылку."
            ))

            return

        await self.request.reply((
            "**Привет**,\n"
            "🔗 Вот твоя ссылка:\n"
            "https://deletelife.ru/vbRU3Dzp2E\n"
            "Отправляй ссылку друзьям, чтобы напугать их."
        ))
