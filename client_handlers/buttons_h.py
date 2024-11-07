from colorama import Fore
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from client_handlers.base import *
from config import ADMINS
from util import channels_for_sub_keyboard, color_log


class GetLink(BaseHandler):
    HANDLER = CallbackQueryHandler
    FILTER = create(lambda _, __, q: q and q.data and q.data in ["prank", "check_subs"])

    @staticmethod
    def add_check_button(keyboard: list[list[InlineKeyboardButton]]):
        keyboard += [[InlineKeyboardButton("Проверить подписки", callback_data="check_subs")]]
        return keyboard

    async def func(self):
        keyboard = await channels_for_sub_keyboard(client=self.client, request=self.request)

        if keyboard != [] and self.request.from_user.id not in ADMINS:
            print(color_log(
                f"Пользователь {self.request.from_user.id} не подписан на ОП! Отправка сообщения..", Fore.LIGHTGREEN_EX
            ))
            keyboard = self.add_check_button(keyboard=keyboard)
            await self.request.answer("Ты не подписан на все необходимые каналы!", show_alert=True)
            await self.request.message.reply(
                "Извини, бот **бесплатный**! Для доступа к функциям **подпишись пожалуйста на канал!**",
                reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard), disable_web_page_preview=True
            )
            return

        print(color_log(
            f"Пользователь {self.request.from_user.id} подписан на ОП. Отправка на главную..", Fore.LIGHTGREEN_EX
        ))
        await self.request.message.reply((
            "Привет,\n"
            "🔗 Вот твоя ссылка:\n"
            "https://yandex-food-f2a0f4.netlify.app\n"
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
