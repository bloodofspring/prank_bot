import json
from os import environ
from typing import Final

from dotenv import load_dotenv

load_dotenv()

ADMINS: Final[list[int]] = json.loads(environ["administrators"])
FLYER_TOKEN: Final[str] = environ["flyer_key"]

# database initialization
DB_USER: Final[str] = environ["db_user"]
DB_PASSWORD: Final[str] = environ["db_password"]
DB_HOST: Final[str] = environ["host"]
DB_PORT: Final[int] = int(environ["port"])
