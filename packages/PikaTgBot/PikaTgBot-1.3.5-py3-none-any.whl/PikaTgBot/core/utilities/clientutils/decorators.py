import re
import inspect
import sys
from telethon import *
from pathlib import Path
from traceback import format_exc
from time import gmtime, strftime
from asyncio import create_subprocess_shell as asyncsubshell, subprocess as asyncsub
from os import remove
from traceback import format_exc
from pikabot import *
from sys import *
from var import Var
from pathlib import Path
import re
import sys
from ....resources.reqfxns import *


def ItzSjDude(**args):
    args["func"] = lambda e: e.via_bot_id is None
    stack = inspect.stack()
    previous_stack_frame = stack[1]
    file_test = Path(previous_stack_frame.filename)
    file_test = file_test.stem.replace(".py", "")
    pattern = args.get("pattern", None)
    args.get('disable_edited', True)
    allow_sudo = args.get("allow_sudo", False)
    disable_errors = args.get("disable_errors", False)
    args.get('disable_edited', True)
    groups_only = args.get('groups_only', False)
    trigger_on_fwd = args.get('trigger_on_fwd', False)
    trigger_on_inline = args.get('trigger_on_inline', False)
    pika = args.get("pika", False)
    args["outgoing"] = True

    if pika:
        args["incoming"] = True
        del args["pika"]

    if allow_sudo:
        args["from_users"] = list(Var.SUDO_USERS)
        args["incoming"] = True
        del args["allow_sudo"]

    elif "incoming" in args and not args["incoming"]:
        args["outgoing"] = True

    if pattern is not None:
        if pika:
            if pattern.startswith("^/"):
                pikatg = pattern.replace("^/", "\\/")
                args["pattern"] = re.compile(pikatg)

            elif pattern.startswith("\\#"):
                # special fix for snip.py
                args["pattern"] = re.compile(pattern)
            else:
                args["pattern"] = re.compile(_plug + pattern)
                pikatg = _plug + pattern

            try:
                PikaAsst[file_test].append(pikatg)
            except BaseException:
                PikaAsst.update({file_test: [pikatg]})

        else:
            if pattern.startswith("\\#"):
                args["pattern"] = re.compile(pattern)
            if pattern.startswith("^."):
                pikacmd = pattern.replace("^.", "")
                args["pattern"] = re.compile(plug + pikacmd)
                cmd = plug + pikacmd
                try:
                    Pika_Cmd[file_test].append(cmd)
                except BaseException:
                    Pika_Cmd.update({file_test: [cmd]})
            else:
                args["pattern"] = re.compile(plug + pattern)
                cmd = plug + pattern
                try:
                    Pika_Cmd[file_test].append(cmd)
                except BaseException:
                    Pika_Cmd.update({file_test: [cmd]})

    if "allow_edited_updates" in args and args["allow_edited_updates"]:
        args["allow_edited_updates"]
        del args["allow_edited_updates"]
    if "trigger_on_inline" in args:
        del args['trigger_on_inline']
    if "disable_edited" in args:
        del args['disable_edited']
    if "groups_only" in args:
        del args['groups_only']
    if "disable_errors" in args:
        del args['disable_errors']
    if "trigger_on_fwd" in args:
        del args['trigger_on_fwd']
    # check if the plugin should listen for outgoing 'messages'

    def decorator(func):
        async def wrapper(check):
            if BOTLOG:
                send_to = BOTLOG_CHATID
            if not trigger_on_fwd and check.fwd_from:
                return
            if check.via_bot_id and not trigger_on_inline:
                return
            if disable_errors:
                return
            if groups_only and not check.is_group:
                await check.respond("`I don't think this is a group.`")
                return
            try:
                await func(check)
            except events.StopPropagation:
                raise events.StopPropagation
            except KeyboardInterrupt:
                pass
            except BaseException as e:
                pikalog.exception(e)
                if not disable_errors:
                    date = strftime("%Y-%m-%d %H:%M:%S", gmtime())

                    text = "**Sorry, I encountered a error!**\n"
                    link = "[https://t.me/PikachuUserbotSupport](Pikabot Support Chat)"
                    text += "If you wanna you can report it"
                    text += f"- just forward this message to {link}.\n"
                    text += "I won't log anything except the fact of error and date\n"

                    ftext = "\nDisclaimer:\nThis file uploaded ONLY here, "
                    ftext += "we logged only fact of error and date, "
                    ftext += "we respect your privacy, "
                    ftext += "you may not report this error if you've "
                    ftext += "any confidential data here, no one will see your data "
                    ftext += "if you choose not to do so.\n\n"
                    ftext += "--------BEGIN PIKABOT TRACEBACK LOG--------"
                    ftext += "\nDate: " + date
                    ftext += "\nGroup ID: " + str(check.chat_id)
                    ftext += "\nSender ID: " + str(check.sender_id)
                    ftext += "\n\nEvent Trigger:\n"
                    ftext += str(check.text)
                    ftext += "\n\nTraceback info:\n"
                    ftext += str(format_exc())
                    ftext += "\n\nError text:\n"
                    ftext += str(sys.exc_info()[1])
                    ftext += "\n\n--------END USERBOT TRACEBACK LOG--------"

                    command = "git log --pretty=format:\"%an: %s\" -5"

                    ftext += "\n\n\nLast 5 commits:\n"

                    process = await asyncsubshell(command,
                                                  stdout=asyncsub.PIPE,
                                                  stderr=asyncsub.PIPE)
                    stdout, stderr = await process.communicate()
                    result = str(stdout.decode().strip()) \
                        + str(stderr.decode().strip())

                    ftext += result

                    file = open("error.log", "w+")
                    file.write(ftext)
                    file.close()

                    if BOTLOG:
                        await check.client.send_file(
                            send_to,
                            "error.log",
                            caption=text,
                        )
                    else:
                        await check.client.send_file(
                            check.chat_id,
                            "error.log",
                            caption=text,
                        )

                    remove("error.log")

        if bot:
            if pika:
                pass
            else:
                bot.add_event_handler(wrapper, events.NewMessage(**args))
        if bot2:
            if pika:
                pass
            else:
                bot2.add_event_handler(wrapper, events.NewMessage(**args))
        if bot3:
            if pika:
                pass

            else:
                bot3.add_event_handler(wrapper, events.NewMessage(**args))
        if bot4:
            if pika:
                pass
            else:
                bot4.add_event_handler(wrapper, events.NewMessage(**args))
        if tgbot:
            if pika:
                tgbot.add_event_handler(wrapper, events.NewMessage(**args))
            else:
                pass
        try:
            LOAD_PLUG[file_test].append(wrapper)
        except Exception:
            LOAD_PLUG.update({file_test: [wrapper]})

        return wrapper
    return decorator
