# Ultroid - UserBot
# Copyright (C) 2020 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.

import os, redis
from telethon.sessions import StringSession
from telethon import TelegramClient
from .dB.database import Var
from .dB.core import *
from logging import basicConfig, getLogger, INFO, DEBUG, warning as wr
from distutils.util import strtobool as sb
from .misc import *
from .utils import *
from .functions import *
from decouple import config
from datetime import datetime

LOGS = getLogger(__name__)

__version__ = "14.2-beta"

if not Var.API_ID or not Var.API_HASH:
    wr("No API_ID or API_HASH found.    Quiting...")
    exit(1)


if Var.SESSION:
    try:
        ultroid_bot = TelegramClient(
            StringSession(Var.SESSION), Var.API_ID, Var.API_HASH
        )
    except Exception as ap:
        wr(f"ERROR - {ap}")
        exit(1)
else:
    wr("No string Session found, Bot Quiting Now !!")
    exit(1)

START_TIME = datetime.now()

try:
    redis_info = Var.REDIS_URI.split(":")
    udB = redis.StrictRedis(
        host=redis_info[0],
        port=redis_info[1],
        password=Var.REDIS_PASSWORD,
        charset="utf-8",
        decode_responses=True,
    )
except BaseException:
    wr("REDIS_URI or REDIS_PASSWORD is wrong! Recheck!")
    wr("Ultroid has shutdown!")
    exit(1)

try:
    if udB.get("HNDLR"):
        HNDLR = udB.get("HNDLR")
    else:
        udB.set("HNDLR", ".")
        HNDLR = udB.get("HNDLR")
except BaseException:
    pass

if udB.get("VC_SESSION"):
    try:
        vcbot = TelegramClient(
            StringSession(udB.get("VC_SESSION")),
            api_id=Var.API_ID,
            api_hash=Var.API_HASH,
        )
    except Exception as ex:
        vcbot = None
else:
    vcbot = None
