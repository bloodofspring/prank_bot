from peewee import BooleanField, BigIntegerField

from database.models.base import BaseModel


class BotUsers(BaseModel):
    telegram_id = BigIntegerField()
    is_subscribed_to_op = BooleanField(default=False)
