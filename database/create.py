from database.db_init import psql_db
from database.models import *


def create_tables() -> None:
    """Database models to tables"""
    if not active_models:
        return
    with psql_db:
        psql_db.create_tables(active_models)
