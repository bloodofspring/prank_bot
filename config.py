import json
from os import environ
from typing import Final

from dotenv import load_dotenv

load_dotenv()

ADMINS: Final[list[int]] = json.loads(environ["administrators"])
