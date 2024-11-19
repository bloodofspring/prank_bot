from database.db_init import db
from database.models import *


def create_tables() -> None:
    """Database models to tables"""
    if not active_models:
        return
    with db:
        db.create_tables(active_models)
