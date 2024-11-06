from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from base import *
from database.models import ChannelsToSub
from util import channels_for_sub_keyboard


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
        keyboard = add_sys_buttons(keyboard=await channels_for_sub_keyboard(client=self.client, request=self.request))
        await self.request.message.reply("Настройка OП", reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard))


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
                keyboard = await channels_for_sub_keyboard(client=self.client, request=self.request, to_remove=True)
                keyboard += [[InlineKeyboardButton("Отмена", callback_data="op_settings")]]
                await self.request.message.reply(
                    "Нажмите на кнопку, которую хотите удалить",
                    reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard)
                )

            case _ as rem if "rem_op" in rem:
                channel_name = rem.split()[0].strip()
                ChannelsToSub.delete_by_id(ChannelsToSub.get(tg_id=channel_name))
                await self.request.message.reply(
                    f"Канал {channel_name} удален!",
                    reply_markup=InlineKeyboardMarkup(
                        [[InlineKeyboardButton("К настройкам ОП", callback_data="op_settings")]]
                    )
                )
