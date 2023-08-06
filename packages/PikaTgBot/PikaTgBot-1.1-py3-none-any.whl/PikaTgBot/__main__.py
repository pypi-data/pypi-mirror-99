#!/usr/bin/env python3
#
# Copyright (C) 2020 by ItzSjDude@Github, < https://github.com/ItzSjDude/PikachuUserbot >.
#
# This file is part of < https://github.com/ItzSjDude/PikachuUserbot > project,
# and is released under the "GNU v3.0 License Agreement".
#
# Please see < https://github.com/ItzSjDude/PikachuUserbot/blob/master/LICENSE >
#
# All rights reserved
from . import *


async def init_pika():
    if bot is None:
        from pikabot.login import pika_login
        pikalog.info(
            "**MAINCLIENT**: Started Login Assistent, Do /start at {}'s PM".format(BF_BOTNAME))
        await pika_login("STRING_SESSION")
    else:
        _const = {}
        _start = True
        Var.CUSTOM_CMD
        from pikabot.login import pika_login, pika_msg
        _logstr_ = "__{}__: Connected 🔥"
        _logstr2_ = "__{}__: Started Login Assistent, Do /start at {}'s PM".format(
            _const, BF_BOTNAME)
        import glob
        path = './plugins/*.py'
        _path = './pikabot/Assistant/plugins/*.py'
        files = glob.glob(path)
        _files = glob.glob(_path)

        if _start:
            await tgbot.start()
            tgbot.me = await tgbot.get_me()
            tgbot.PikaAsst = {}
            tgbot.uid = telethon.utils.get_peer_id(tgbot.me)
            pikalog.info(_logstr_.format("TGBOT"))
            msg = _logstr_.format("_TGBOT_") + '\n\n'
            _logpika = await tgbot.send_message(BOTLOG_CHATID, msg)
            if bot:
                try:
                    await bot.start()
                    cli1 = await client.get_messages(Client, None, filter=InputMessagesFilterDocument)
                    total = int(cli1.total)
                    total_doxx = range(0, total)
                    for ixo in total_doxx:
                        mxo = cli1[ixo].id
                        await client.download_media(await bot.get_messages(Client, ids=mxo), "pikabot/main_plugs")

                    bot.me = await bot.get_me()
                    bot.pika_cmd = {}
                    bot.uid = telethon.utils.get_peer_id(bot.me)
                    pikalog.info(_logstr_.format("MAINCLIENT"))
                    msg += _logstr_.format("MAINCLIENT") + "\n\n"
                    await pika_msg(_logpika, msg)
                except Exception as e:
                    pikalog.info(str(e))
                    pikalog.info(_logstr2_.format("MAINCLIENT"))
                    msg += _logstr2_.format("MAINCLIENT") + "\n\n"
                    await pika_msg(_logpika, msg)
                    await pika_login("STRING_SESSION")

            if bot2:
                try:
                    await bot2.start()
                    pikalog.info(_logstr_.format("MULTICLIENT1"))
                    bot2.me = await bot2.get_me()
                    bot2.uid = telethon.utils.get_peer_id(bot2.me)
                    msg += _logstr_.format("MULTICLIENT1") + "\n\n"
                    await pika_msg(_logpika, msg)
                except BaseException:
                    pikalog.info(_logstr2_.format("MULTICLIENT1"))
                    msg += _logstr2_.format("MULTICLIENT1") + "\n\n"
                    await pika_msg(_logpika, msg)
                    await pika_login("STR2")
            if bot3:
                try:
                    await bot3.start()
                    pikalog.info(_logstr2_.format("MULTICLIENT2"))
                    bot3.me = await bot3.get_me()
                    bot3.uid = telethon.utils.get_peer_id(bot3.me)
                    msg += _logstr_.format("MULTICLIENT2") + "\n\n"
                    await pika_msg(_logpika, msg)
                except BaseException:
                    pikalog.info(_logstr2_.format("MULTICLIENT2"))
                    msg += _logstr2_.format("MULTICLIENT2") + "\n\n"
                    await pika_msg(_logpika, msg)
                    await pika_login("STR3")
            if bot4:
                try:
                    await bot4.start()
                    pikalog.info(_logstr_.format("MULTICLIENT3"))
                    bot4.me = await bot4.get_me()
                    bot4.uid = telethon.utils.get_peer_id(bot4.me)
                    msg += logstr_.format("MULTICLIENT3") + "\n\n"
                    await pika_msg(_logpika, msg)
                except BaseException:
                    pikalog.info(_logstr2_.format("MULTICLIENT3"))
                    msg += _logstr2_.format("MULTICLIENT3") + "\n\n"
                    await pika_msg(_logpika, msg)
                    await pika_login("STR4")

            if Var.STR1 and bot is None:
                pikalog.info(
                    "**MAINCLIENT**: Session Expired / Invalid, Started Login Assistent, Do /start at {}'s PM".format(BF_BOTNAME))
                await pika_login("STRING_SESSION")

            if Var.STR2 and bot2 is None:
                pikalog.info(
                    "**MULTICLIENT1**: Session Expired / Invalid, Started Login Assistent, Do /start at {}'s PM".format(BF_BOTNAME))
                await pika_login("STR2")

            if Var.STR3 and bot3 is None:
                pikalog.info(
                    "**MULTICLIENT2**: Session Expired / Invalid, Started Login Assistent, Do /start at {}'s PM".format(BF_BOTNAME))
                await pika_login("STR3")

            if Var.STR4 and bot4 is None:
                pikalog.info(
                    "**MULTICLIENT3**: Session Expired, Started Login Assistent, Do /start at {}'s PM".format(BF_BOTNAME))
                await pika_login("STR4")

            def __load_plugs__():
                from pikabot.utils import pika_plugins, pika_assistant
                for name in files:
                    with open(name) as f:
                        path1 = Path(f.name)
                        shortname = path1.stem
                        pika_plugins(shortname.replace(".py", ""))

                for name in _files:
                    with open(name) as f:
                        _asstpath = Path(f.name)
                        shortname = _asstpath.stem
                        pika_assistant(shortname.replace(".py", ""))
            __load_plugs__()

            msg += "Sucessfully Loaded Plugins\n\n"
            await pika_msg(_logpika, msg)
            from ._core import _verify
            await _verify()
            msg += "**Pikabot Started Sucessfully**"
            await pika_msg(_logpika, msg)

        if len(argv) not in (1, 3, 4):
            if bot:
                await bot.disconnect()
            if bot2:
                await bot2.disconnect()
            if bot3:
                await bot3.disconnect()
            if bot4:
                await bot4.disconnect()
        else:
            if bot:
                await bot.run_until_disconnected()
            if bot2:
                await bot2.run_until_disconnected()
            if bot3:
                await bot3.run_until_disconnected()
            if bot4:
                await bot4.run_until_disconnected()


if __name__ == "__main__":
    pikaloop = asyncio.get_event_loop()
    pikaloop.run_until_complete(init_pika())
