from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from client_handlers.base import *
from filters import is_admin


class StartCmd(BaseHandler):
    FILTER = command("start")

    def add_config_button_if_admin(self, keyboard: list[list[InlineKeyboardButton]]):
        if not is_admin(None, None, m=self.request):
            return keyboard

        keyboard += [[InlineKeyboardButton("Настроить ОП", callback_data="op_settings")]]

        return keyboard

    async def func(self):
        keyboard = [
            [InlineKeyboardButton("Пранкануть друга", callback_data="prank")],
            [InlineKeyboardButton("Как работает бот", callback_data="how_d_it_works")],
            [InlineKeyboardButton("Наш канал", url="https://t.me/Prankston")],
        ]
        keyboard = self.add_config_button_if_admin(keyboard=keyboard)

        await self.request.reply((
            "Привет, это @PrankerStonbot\n"
            "Выбери действие."
        ), reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard))
