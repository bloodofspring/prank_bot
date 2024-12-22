import sys

from database.models import BotUsers


def main():
    if input("База данных ДОЛЖНА быть создана перед запуском этого файла. Вы уверены, что хотите продолжить? [Y/n]: ") != "Y":
        exit("Process terminated by user, exit code: 0")

    stdin = tuple(map(int, map(str.strip, sys.stdin)))

    for uid in stdin:
        if BotUsers.get_or_none(tg_id=uid) is not None:
            continue

        BotUsers.create(
            tg_id=uid,
            is_subscribed_to_op=True,
        )


if __name__ == "__main__":
    main()
