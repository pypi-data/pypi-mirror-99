from telethon.sessions import StringSession
from telethon import TelegramClient
from ..core.database import pdb
if pdb.maincl:
    bot = client = TelegramClient(
        StringSession(
            pdb.maincl),
        pdb.api_id,
        pdb.api_hash,
        auto_reconnect=True)
else:
    bot = client = None

if pdb.multicl1:
    bot2 = client2 = TelegramClient(
        StringSession(
            pdb.multicl1),
        pdb.api_id,
        pdb.api_hash,
        auto_reconnect=True)
else:
    bot2 = client2 = None

if pdb.multicl2:
    bot3 = client3 = TelegramClient(
        StringSession(
            pdb.multicl2),
        pdb.api_id,
        pdb.api_hash,
        auto_reconnect=True)
else:
    bot3 = None
if pdb.multicl3:
    bot4 = client4 = TelegramClient(
        StringSession(
            pdb.multicl3),
        pdb.api_id,
        pdb.api_hash,
        auto_reconnect=True)
else:
    bot4 = client4 = None

if pdb.bf_token:
    tgbot = tgbot_client = TelegramClient(
        "PikaTgbot", pdb.api_id, pdb.api_hash).start(
        bot_token=pdb.bf_token)
else:
    tgbot = tgbot_client = None
