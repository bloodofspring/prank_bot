"""Run this file to start bot"""
import os

from dotenv import load_dotenv

from colorama import Fore
from bot import client
from client_handlers import active_handlers
from database.create import create_tables


def add_handlers() -> None:
    for handler in active_handlers:
        client.add_handler(handler().de_pyrogram_handler)


def remove_bot_journals() -> None:
    load_dotenv()
    if os.path.exists(f"{os.environ['name']}.session"):
        os.remove(f"{os.environ['name']}.session")

    if os.path.exists(f"{os.environ['name']}.session-journal"):
        os.remove(f"{os.environ['name']}.session-journal")


def run_bot() -> None:
    add_handlers()
    create_tables()
    remove_bot_journals()
    client.run()


if __name__ == "__main__":
    run_bot()
