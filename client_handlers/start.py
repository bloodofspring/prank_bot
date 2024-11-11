from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from client_handlers.base import *


class StartCmd(BaseHandler):
    FILTER = command("start")

    async def func(self):
        keyboard = [
            [InlineKeyboardButton("Пранкануть друга", callback_data="prank")],
            [InlineKeyboardButton("Как работает бот", callback_data="how_d_it_works")],
            [InlineKeyboardButton("Наш канал", url="https://t.me/Prankston")],
        ]

        await self.request.reply((
            "Привет, это @PrankerStonbot\n"
            "Выбери действие."
        ), reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard))
