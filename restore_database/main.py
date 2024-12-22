import sys

from database.create import create_tables
from database.models import BotUsers

create_tables()


def main():
    stdin = tuple(map(int, map(str.strip, sys.stdin)))

    for uid in stdin:
        if BotUsers.get_or_none(tg_id=uid) is not None:
            continue

        BotUsers.create(
            tg_id=uid,
            is_subscribed_to_op=True,
        )


main()
