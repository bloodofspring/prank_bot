from typing import Final

from peewee import PostgresqlDatabase

from config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

psql_db: Final[PostgresqlDatabase] = PostgresqlDatabase(
    "botData",
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)
