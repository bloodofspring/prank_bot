import json
from os import environ
from typing import Final

from dotenv import load_dotenv

load_dotenv()

OP_USERS: Final[list[int]] = json.loads(environ["administrators"])
