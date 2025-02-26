from peewee import PostgresqlDatabase

from config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

psql_db: PostgresqlDatabase = PostgresqlDatabase(
    "prankBotDb",
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)

def update_connection():
    global psql_db

    psql_db = PostgresqlDatabase(
        "prankBotDb",
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
