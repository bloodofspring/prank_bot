import peewee
import psycopg2
from colorama import Fore
from pyrogram import Client
from pyrogram import filters, types
from pyrogram.filters import command, all_filter, regex, create
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from pyrogram.handlers.handler import Handler
from pyrogram.types import CallbackQuery

from database.models.users import BotUsers
from database.db_init import update_connection
from util import color_log

from config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

request_type = types.Message | types.CallbackQuery  # add some types here if you need:3
__all__ = [
    "BaseHandler", "request_type", "Client",
    "command", "all_filter", "regex", "create",
    "MessageHandler", "CallbackQueryHandler",
]


class BaseHandler:
    """Базовый обработчик-исполнитель"""
    __name__ = ""
    HANDLER: Handler = MessageHandler
    FILTER: filters.Filter | None = None

    def __init__(self):
        self.request: request_type | None = None
        self.client: Client | None = None
        self.db_user = None

    @property
    def de_database(self):
        try:
            request = self.request.message if isinstance(self.request, CallbackQuery) else self.request
            db_user, created = BotUsers.get_or_create(telegram_id=request.chat.id)
            if created:
                print(color_log(
                    f"Пользователь {request.chat.id} занесен в базу данных! Всего пользователей: {len(BotUsers.select())}",
                    Fore.LIGHTGREEN_EX
                ))
        except (peewee.InterfaceError, psycopg2.InterfaceError):
            update_connection()
            return self.de_database

        return db_user

    async def func(self):
        raise NotImplementedError

    async def execute(self, client: Client, request: request_type):
        self.request = request
        self.client = client
        self.db_user = self.de_database

        await self.func()

    @property
    def de_pyrogram_handler(self):
        return self.HANDLER(self.execute, self.FILTER)
