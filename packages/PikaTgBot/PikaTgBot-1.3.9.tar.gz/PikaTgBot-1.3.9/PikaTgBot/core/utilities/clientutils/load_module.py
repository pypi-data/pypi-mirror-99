from telethon import *
from importlib.util import *
from ....resources.reqfxns import *


def load_all_modules(shortname):
    if shortname.startswith("__"):
        pass
    else:
        path = Path(f"plugins/{shortname}.py")
        name = "plugins.{}".format(shortname)
        spec = spec_from_file_location(name, path)
        mod = module_from_spec(spec)
        mod.bot = bot
        mod.Var = Var
        mod.rx = rx
        mod.command = ItzSjDude
        mod.ItzSjDude = ItzSjDude
        mod.logger = logging.getLogger(shortname)
        sys.modules["SysRuntime"] =
        sys.modules["userbot"] = pikabot
        sys.modules["userbot.utils"] = pikabot.utils
        mod.Config = Var
        mod.borg = bot
        sys.modules["uniborg.util"] = pikabot.utils
        # support for paperplaneextended
        spec.loader.exec_module(mod)
        bot.pika_cmd[shortname] = mod
        # for imports
        sys.modules["pikabot" + shortname] = mod
        logpl.info("Successfully (re)imported " + shortname)


def load_ext_module(shortname):
    if shortname.endswith("_"):
        from pathlib import Path
        path = Path(f"plugins/{shortname}.py")
        name = "plugins.{}".format(shortname)
        spec = spec_from_file_location(name, path)
        mod = module_from_spec(spec)
        spec.loader.exec_module(mod)


def remove_plugin(shortname):
    try:
        try:
            for i in LOAD_PLUG[shortname]:
                if bot is not None:
                    bot.remove_event_handler(i)
                if bot2 is not None:
                    bot2.remove_event_handler(i)
                if bot3 is not None:
                    bot3.remove_event_handler(i)
                if bot4 is not None:
                    bot4.remove_event_handler(i)
            del LOAD_PLUG[shortname]

        except BaseException:
            name = f"plugins.{shortname}"
            if bot is not None:
                for i in reversed(range(len(bot._event_builders))):
                    ev, cb = bot._event_builders[i],
                    if cb.__module__ == name:
                        del bot._event_builders[i]
            if bot2 is not None:
                for i in reversed(range(len(bot2._event_builders))):
                    ev, cx = bot2._event_builders[i],
                    if cx.__module__ == name:
                        del bot2._event_builders[i]
            if bot3 is not None:
                for i in reversed(range(len(bot3._event_builders))):
                    ev, cy = bot3._event_builders[i],
                    if cy.__module__ == name:
                        del bot3._event_builders[i]
            if bot4 is not None:
                for i in reversed(range(len(bot4._event_builders))):
                    ev, cz = bot4._event_builders[i],
                    if cz.__module__ == name:
                        del bot4._event_builders[i]
    except BaseException:
        raise ValueError
