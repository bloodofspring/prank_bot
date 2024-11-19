from colorama import Fore
from flyerapi import Flyer
from pyrogram.types import InlineKeyboardButton

from client_handlers.base import *
from config import FLYER_TOKEN
from database.models import BotUsers
from util import color_log


class GetLink(BaseHandler):
    HANDLER = CallbackQueryHandler
    FILTER = create(lambda _, __, q: q and q.data and q.data in ["prank", "check_subs"])

    @staticmethod
    def add_check_button(keyboard: list[list[InlineKeyboardButton]]):
        keyboard += [[InlineKeyboardButton("Проверить подписки", callback_data="check_subs")]]
        return keyboard

    async def func(self):
        flyer = Flyer(FLYER_TOKEN)
        if not await flyer.check(self.request.from_user.id):
            print(color_log(
                f"Пользователь {self.request.from_user.id} не подписан на ОП! Отправка сообщения..",
                Fore.LIGHTGREEN_EX
            ))
            db_user = self.db_user
            db_user.is_subscribed_to_op = False
            BotUsers.save(db_user)

            return

        db_user = self.db_user
        db_user.is_subscribed_to_op = True
        BotUsers.save(db_user)

        print(color_log(
            f"Пользователь {self.request.from_user.id} подписан на ОП. Отправка на главную..", Fore.LIGHTGREEN_EX
        ))

        subscribed = len(BotUsers.select().where(BotUsers.is_subscribed_to_op))
        all_ = len(BotUsers.select())
        percent = '{:.2f}%'.format(round((subscribed / all_) * 100, 2))
        print(color_log(f"Подписанных на ОП пользователей: {subscribed}/{all_} ({percent})", Fore.LIGHTCYAN_EX))

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
