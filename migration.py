from peewee import BooleanField
from playhouse.migrate import SqliteMigrator, migrate

from database import db
from database.models import BotUsers


def print_data_2():
    print(*map(lambda x: f"{x.tg_id} -- {x.is_subscribed_to_op}", BotUsers.select()), sep="\n")


def mig():
    migrator = SqliteMigrator(db)

    migrate(
        migrator.add_column("BotUsers", "is_subscribed_to_op", BooleanField(default=False)),
    )
    for u in BotUsers.select():
        u.is_subscribed_to_op = True
        BotUsers.save(u)


mig()
print_data_2()
