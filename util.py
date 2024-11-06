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
