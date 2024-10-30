from peewee import IntegerField, BooleanField, ForeignKeyField

from database.models.base import BaseModel


class BotUsers(BaseModel):
    tg_id = IntegerField()


class BotUserConfig(BaseModel):
    is_authorized = BooleanField()

    user = ForeignKeyField(BotUsers, backref="config")
