from colorama import Fore
from peewee import OperationalError
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from client_handlers.base import *
from database.models import ChannelsToSub
from util import all_op_keyboard, color_log


def add_sys_buttons(keyboard: list[list[InlineKeyboardButton]]) -> list[list[InlineKeyboardButton]]:
    keyboard += [[
        InlineKeyboardButton("Добавить", callback_data="add_op"),
        InlineKeyboardButton("Удалить", callback_data="rem_op")
    ]]

    return keyboard


class OpSettings(BaseHandler):
    HANDLER = CallbackQueryHandler
    FILTER = create(lambda _, __, q: q and q.data and q.data == "op_settings")

    async def func(self):
        keyboard = add_sys_buttons(keyboard=all_op_keyboard(remove=False))
        await self.request.message.reply(
            f"Настройка OП. Добавлено каналов: {len(keyboard) - 1}",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard)
        )


class ChangeOpConfig(BaseHandler):
    HANDLER = CallbackQueryHandler
    FILTER = create(lambda _, __, q: q and q.data and q.data.split()[0] in ["add_op", "rem_op"])

    async def func(self):
        match self.request.data:
            case "add_op":
                await self.request.message.reply(
                    "Перешлите ниже ссылку на канал в формате @username",
                    reply_markup=InlineKeyboardMarkup(
                        [[InlineKeyboardButton("Отмена", callback_data="op_settings")]]
                    )
                )

            case "rem_op":
                keyboard = all_op_keyboard(remove=True)
                keyboard += [[InlineKeyboardButton("Отмена", callback_data="op_settings")]]
                await self.request.message.reply(
                    "Нажмите на кнопку, которую хотите удалить",
                    reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard)
                )

            case _ as rem if "rem_op" in rem:
                channel_name = rem.split()[1].strip()
                ChannelsToSub.delete_by_id(ChannelsToSub.get(tg_id=channel_name))
                print(color_log(f"Канал {channel_name} был удален из списка ОП!", Fore.LIGHTGREEN_EX))
                await self.request.message.reply(
                    f"Канал {channel_name} удален!",
                    reply_markup=InlineKeyboardMarkup(
                        [[InlineKeyboardButton("К настройкам ОП", callback_data="op_settings")]]
                    )
                )


class ChannelUsernameDownloader(BaseHandler):
    FILTER = create(lambda _, __, m: m and m.text and "@" in m.text)

    def url_is_valid(self):
        return (ChannelsToSub.get_or_none(tg_id=self.request.text) is None and len(self.request.text) <= 34 and
                self.request.text.startswith("@") and len(self.request.text.split()) == 1)

    async def func(self):
        if not self.url_is_valid():
            return

        try:
            await self.client.get_chat(chat_id=self.request.text)
            ChannelsToSub.create(tg_id=self.request.text)
        except (OperationalError, ValueError, Exception):
            return

        print(color_log(f"Канал {self.request.text} был добавлен в список ОП!", Fore.LIGHTGREEN_EX))
        await self.request.reply(
            f"Канал {self.request.text} добавлен в список ОП!",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("К настройкам", callback_data="op_settings")]]
            )
        )
