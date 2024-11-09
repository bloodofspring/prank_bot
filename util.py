from datetime import datetime

from colorama import Fore
from pyrogram import Client
from pyrogram.types import InlineKeyboardButton, CallbackQuery

from client_handlers.base import request_type
from database.models import ChannelsToSub


async def channels_for_sub_keyboard(client: Client, request: request_type) -> (list[list[InlineKeyboardButton]]):
    user_id = request.message.chat.id if isinstance(request, CallbackQuery) else request.chat.id
    keyboard = []

    for n, chan in enumerate(ChannelsToSub.select(), start=1):
        try:
            await client.get_chat_member(chat_id=chan.tg_id, user_id=user_id)
            keyboard.append([InlineKeyboardButton(text=f"Канал {n}", url=f"https://t.me/{chan.tg_id.strip('@')}")])
        except Exception as e:
            can_t_get_user_error = e

    return keyboard


def get_all_op(remove: bool):
    keyboard = []

    for chan in ChannelsToSub.select():
        if remove:
            keyboard.append([InlineKeyboardButton(text=f"Канал {chan.ID}", callback_data=f"rem_op {chan.tg_id}")])
            continue

        keyboard.append([
            InlineKeyboardButton(text=f"Канал {chan.ID} ({chan.tg_id})", url=f"https://t.me/{chan.tg_id.strip('@')}")
        ])


def color_log(text: str, colors: str | list[str], head_c: str = Fore.LIGHTWHITE_EX, separator: str = " ") -> str:
    now = datetime.now()
    now_shorted = f"{now.year}-{now.month}-{now.day} {now.hour}:{now.minute}:{now.second}"

    if not isinstance(colors, list):
        return head_c + f"[{now_shorted}]: >> " + colors + text

    parts = text.split(separator)
    res = ""
    for w, c in zip(parts, colors):
        res += c + w + " "

    if len(parts) > len(colors):
        res += colors[-1] + res[len(colors) - 1:]

    return head_c + f"[{now_shorted}]: >> " + res
