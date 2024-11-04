from argparse import ArgumentParser

from database.create import create_tables
from database.models import ChannelsToSub


def main():
    parser = ArgumentParser()
    parser.add_argument("-au", "--add_username", help="Удалить из списка для подписки [@username канала]", type=str)
    parser.add_argument("-du", "--drop_username", help="Добавить в список для подписки [@username канала]", type=str)

    args = parser.parse_args()
    create_tables()
    try:
        if args.add_username:
            ChannelsToSub.create(tg_id=args.username)
        if args.drop_username:
            ChannelsToSub.delete_by_id(ChannelsToSub.get(tg_id=args.drop_username))
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
