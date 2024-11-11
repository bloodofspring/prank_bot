from datetime import datetime

from colorama import Fore
from pyrogram.types import InlineKeyboardButton


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
