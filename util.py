from datetime import datetime

from colorama import init, Fore
from pyrogram import Client
from pyrogram.types import InlineKeyboardButton, Message, CallbackQuery

from database.models import ChannelsToSub


async def channels_for_sub_keyboard(client: Client, request: Message | CallbackQuery, to_remove: bool = False) -> (
list[list[InlineKeyboardButton]]):
    sub_instances = []

    user_id = request.message.chat.id if isinstance(request, CallbackQuery) else request.chat.id

    for chan in ChannelsToSub.select():
        try:
            await client.get_chat_member(chat_id=chan.tg_id, user_id=user_id)
        except Exception as e:
            can_t_get_user_error = e
            sub_instances.append(chan)

    if not sub_instances:
        return []

    keyboard = []
    for c in sub_instances:
        if to_remove:
            keyboard.append([
                InlineKeyboardButton(text=f"Канал {sub_instances.index(c) + 1}", callback_data=f"rem_op {c.tg_id}")
            ])
            continue

        keyboard.append([
            InlineKeyboardButton(text=f"Канал {sub_instances.index(c) + 1}", url=f"https://t.me/{c.tg_id.strip('@')}")
        ])

    return keyboard


def color_log(text: str, colors: str | list[str], head_c: str = Fore.LIGHTGREEN_EX, separator: str = " ") -> str:
    init(autoreset=True)
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
