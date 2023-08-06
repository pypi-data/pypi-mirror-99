
# ©ItzSjDude
def pikatgbot(pika=None, silent=None):
    def decorator(func):
        @wraps(func)
        async def wrapper(event):
            _selfpika = await tgbot.get_me()
            if "AdmOnly" in pika:
                _pika = await tgbot.get_permissions(int(event.chat_id), event.sender_id)
                if _pika.is_admin:
                    await func(event)
                if event.sender_id == bot.uid:
                    pass
                if not _pika.is_admin:
                    if silent is None:
                        await event.reply("You need to be admin to use this command")

            if "AmIAdm" in pika:

                _pika = await tgbot.get_permissions(int(event.chat_id), _selfpika.id)
                if _pika.is_admin:
                    await func(event)
                else:
                    if silent is None:
                        await event.reply("I am not Admin Nibba😷")

            if "OwnSudo" in pika:
                tgbotusers = list(TGBOT_USERS)
                if event.sender_id == bot.uid or event.sender_id in tgbotusers:
                    await func(event)
                else:
                    if silent is None:
                        await event.reply("**Error**: You are not a Sudo User, Owner.")

            if "Owner" in pika:
                if event.sender_id == bot.uid:
                    await func(event)
                else:
                    if silent is None:
                        await event.reply("Only Owners can execute this Cmd")

            if "BotSudo" in pika:
                if event.sender_id in list(TGBOT_USERS):
                    await func(event)

        return wrapper

    return decorator
