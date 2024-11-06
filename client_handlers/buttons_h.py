from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from client_handlers.base import *
from config import OP_USERS
from database.models import ChannelsToSub


class GetLink(BaseHandler):
    HANDLER = CallbackQueryHandler
    FILTER = create(lambda _, __, q: q and q.data and q.data in ["prank", "check_subs"])

    @property
    async def channels_for_sub_keyboard(self) -> InlineKeyboardMarkup | None:
        sub_instances = []

        for chan in ChannelsToSub.select():
            try:
                await self.client.get_chat_member(chat_id=chan.tg_id, user_id=self.request.from_user.id)
            except Exception as e:
                can_t_get_user_error = e
                sub_instances.append(chan)

        if not sub_instances:
            return None

        return InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text=f"Канал {sub_instances.index(c) + 1}", url=f"https://t.me/{c.tg_id.strip('@')}")
        ] for c in sub_instances])

    @staticmethod
    def add_check_button(keyboard: list[list[InlineKeyboardButton]]):
        keyboard += [InlineKeyboardButton("Проверить подписки", callback_data="check_subs")]
        return keyboard

    async def func(self):
        keyboard = await self.channels_for_sub_keyboard

        if keyboard is not None and self.request.from_user.id not in OP_USERS:
            await self.request.message.reply(
                "Извини, бот **бесплатный**! Для доступа к функциям **подпишись пожалуйста на канал!**",
                reply_markup=keyboard, disable_web_page_preview=True
            )
            return

        await self.request.message.reply((
            "Привет,\n"
            "🔗 Вот твоя ссылка:\n"
            "https: // yandex-food-f2a0f4.netlify.app\n"
            "Отправляй ссылку друзьям, чтобы напугать их."
        ))


class HowDItWorks(BaseHandler):
    HANDLER = CallbackQueryHandler
    FILTER = create(lambda _, __, q: q and q.data and q.data == "how_d_it_works")

    async def func(self):
        await self.request.message.reply((
            "Вы присылаете другу ссылку, которую вам прислал бот.\n"
            "Друг переходит по ссылке и нажимает на кнопку «показать промокод», "
            "но вместо промокода ваш друг будет слушать стоны на всю комнату."
        ))
