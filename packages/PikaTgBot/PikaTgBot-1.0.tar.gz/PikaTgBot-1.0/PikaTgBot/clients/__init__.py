from telethon.sessions import StringSession
from telethon import TelegramClient

if Var.STR1:
    bot = client = TelegramClient(
        StringSession(
            Var.STR1),
        Var.APP_ID,
        Var.API_HASH,
        auto_reconnect=True)
else:
    bot = client = None

if Var.STR2:
    bot2 = client2 = TelegramClient(
        StringSession(
            Var.STR2),
        Var.APP_ID,
        Var.API_HASH,
        auto_reconnect=True)
else:
    bot2 = client2 = None
if Var.STR3:
    bot3 = client3 = TelegramClient(
        StringSession(
            Var.STR3),
        Var.APP_ID,
        Var.API_HASH,
        auto_reconnect=True)
else:
    bot3 = None
if Var.STR4:
    bot4 = client4 = TelegramClient(
        StringSession(
            Var.STR4),
        Var.APP_ID,
        Var.API_HASH,
        auto_reconnect=True)
else:
    bot4 = client4 = None

if BF_BOT:
    tgbot = tgbot_client = TelegramClient(
        "PikaTgbot", Var.APP_ID, Var.API_HASH).start(
        bot_token=BF_BOT)
else:
    tgbot = tgbot_client = None
