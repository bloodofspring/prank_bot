from pyrogram import filters

from config import ADMINS

is_admin_filter = filters.create(lambda _, __, m: m and m.from_user and m.from_user.id in ADMINS)
