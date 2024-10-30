from pyrogram import Client
from pyrogram import filters, types
from pyrogram.filters import command, all_filter, regex, create
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from pyrogram.handlers.handler import Handler

from database.models.users import BotUserConfig, BotUsers

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
        self.request: types.Message | None = None
        self.client: Client | None = None
        self.db_user = None

    @property
    def de_database(self):
        db_user, created = BotUsers.get_or_create(tg_id=self.request.from_user.id)
        if created:
            BotUserConfig.create(is_authorized=False, user=db_user)

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
