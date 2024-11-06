from colorama import Fore

from database.db_init import db
from database.models import *
from util import color_log


def create_tables() -> None:
    """Database models to tables"""
    if not active_models:
        return
    with db:
        db.create_tables(active_models)

    print(color_log("База данных проинициализирована!", Fore.LIGHTGREEN_EX, head_c=Fore.LIGHTYELLOW_EX))
