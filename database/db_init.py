from typing import Final

from peewee import PostgresqlDatabase

from config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
from playhouse.shortcuts import ReconnectMixin

class ReconnectPSQLDatabase(ReconnectMixin, PostgresqlDatabase):
    pass

psql_db: Final[ReconnectPSQLDatabase] = ReconnectPSQLDatabase(
    "testDb",  # prankBotDb
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)
