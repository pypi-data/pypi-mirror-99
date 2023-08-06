__title__ = 'BotAmino'
__author__ = 'ThePhoenix78'
__license__ = 'MIT'
__copyright__ = 'Copyright 2021-2021 ThePhoenix78'
__version__ = '1.7.3.2'
from json import loads
from requests import get

__newest__ = loads(get("https://pypi.python.org/pypi/BotAmino/json").text)["info"]["version"]

if __version__ != __newest__:
    print(f"New version of {__title__} available: {__newest__} (Using {__version__})")

from .BotAmino import *

print(f"version : {__version__}")
