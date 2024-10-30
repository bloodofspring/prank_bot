from peewee import CharField

from database.models.base import BaseModel


class ChannelsToSub(BaseModel):
    tg_id = CharField()  # text usernames only, завезу поддержку приватных каналов позже
