from peewee import IntegerField, BooleanField

from database.models.base import BaseModel


class BotUsers(BaseModel):
    tg_id = IntegerField()
    is_subscribed_to_op = BooleanField(default=False)
