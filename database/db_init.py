from typing import Final

from peewee import SqliteDatabase

db: Final[SqliteDatabase] = SqliteDatabase("bot_data.sqlite")
