from pyrogram import Client
from pyrogram.types import InlineKeyboardButton, Message, CallbackQuery

from database.models import ChannelsToSub


async def channels_for_sub_keyboard(client: Client, request: Message | CallbackQuery, to_remove: bool = False) -> (
        list[list[InlineKeyboardButton]] | None):
    sub_instances = []

    if isinstance(request, CallbackQuery):
        request = request.message

    for chan in ChannelsToSub.select():
        try:
            await client.get_chat_member(chat_id=chan.tg_id, user_id=request.from_user.id)
        except Exception as e:
            can_t_get_user_error = e
            sub_instances.append(chan)

    if not sub_instances:
        return None

    keyboard = []
    for c in sub_instances:
        data = {f"rem_op {c.tg_id}" if to_remove else "url": f"https://t.me/{c.tg_id.strip('@')}"}
        keyboard.append([InlineKeyboardButton(text=f"Канал {sub_instances.index(c) + 1}", **data)])

    return keyboard
