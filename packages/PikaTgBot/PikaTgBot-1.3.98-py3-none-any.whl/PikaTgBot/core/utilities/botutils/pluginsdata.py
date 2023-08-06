import asyncio
import html
import io
import json
import math
import os
import random
import re
import subprocess
import sys
import time
import traceback
import urllib.parse
from asyncio import sleep
from datetime import datetime as pikatime
from os import remove
from random import choice, randint, uniform
from re import findall
from subprocess import PIPE, Popen
from time import sleep
from urllib.parse import quote_plus

import bs4
import heroku3
import pikabot.sql_helper.gmute_sql as gban_sql
import pyfiglet
import pygments
import requests
import speedtest
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim
from humanize import naturalsize
from pikabot.utils import get_readable_time as grt
from PIL import Image, ImageColor, ImageEnhance, ImageOps
from pygments.formatters import ImageFormatter
from pygments.lexers import Python3Lexer
from requests import get
from search_engine_parser import GoogleSearch
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from telegraph import Telegraph, exceptions, upload_file
from telethon import *
from telethon import custom, events
from telethon.errors import (
    BadRequestError,
    ChatAdminRequiredError,
    FloodWaitError,
    ImageProcessFailedError,
    PhotoCropSizeSmallError,
    UserAdminInvalidError,
)
from telethon.errors.rpcerrorlist import (
    MessageTooLongError,
    UserIdInvalidError,
    YouBlockedUserError,
)
from telethon.events.callbackquery import CallbackQuery as Pika_CallBack
from telethon.tl import functions, types
from telethon.tl.functions.channels import (
    EditAdminRequest,
    EditBannedRequest,
    EditPhotoRequest,
)
from telethon.tl.functions.messages import (
    EditChatDefaultBannedRightsRequest,
    SaveDraftRequest,
    UpdatePinnedMessageRequest,
)
from telethon.tl.functions.photos import DeletePhotosRequest, GetUserPhotosRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import (
    ChannelParticipantAdmin,
    ChannelParticipantCreator,
    ChannelParticipantsAdmins,
    ChatAdminRights,
    ChatBannedRights,
    DocumentAttributeFilename,
    InputPhoto,
    MessageEntityMentionName,
    MessageMediaPhoto,
)
from telethon.utils import get_input_location, pack_bot_file_id
from var import Var
from var import Var as Config

CARBONLANG = "auto"
LANG = "en"

try:
    from pikabot import bot, bot2, bot3, bot4
except BaseException:
    pass
try:
    tgbot = bot.tgbot
except BaseException:
    pass
b1 = bot.me
if bot2:
    b2 = bot2.me
else:
    b2 = b1
if bot3:
    b3 = bot3.me
else:
    b3 = b1
if bot4:
    b4 = bot4.me
else:
    b4 = b1

emoji = os.environ.get("INLINE_EMOJI", "")
incols = int(os.environ.get("INLINE_COLUMNS", 3))
inrows = int(os.environ.get("INLINE_ROWS", 7))
rx = Var.CUSTOM_CMD
if emoji is not None:
    xl = emoji
else:
    xl = ""
if incols is not None:
    pikcl = incols
else:
    pikcl = 3

if inrows is not None:
    pikrws = inrows
else:
    pikrws = 7

_emo_ = ["☉", "★", "✗", "✘", "☛", "☞", "✦", "✧", "✪", "✫"]

# ===================== Constants ===========================
PP_TOO_SMOL = "`The image is too small`"
PP_ERROR = "`Failure while processing the image`"
NO_ADMIN = "`I am not an admin!`"
NO_PERM = "`I don't have sufficient permissions!`"
NO_SQL = "`Running on Non-SQL mode!`"

CHAT_PP_CHANGED = "`Chat Picture Changed`"
CHAT_PP_ERROR = (
    "`Some issue with updating the pic,`"
    "`maybe coz I'm not an admin,`"
    "`or don't have enough rights.`"
)
INVALID_MEDIA = "`Invalid Extension`"

BANNED_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True,
)

UNBAN_RIGHTS = ChatBannedRights(
    until_date=None,
    send_messages=None,
    send_media=None,
    send_stickers=None,
    send_gifs=None,
    send_games=None,
    send_inline=None,
    embed_links=None,
)

MUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=True)

UNMUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=False)
# ================================================

GITHUB = "https://github.com"
DEVICES_DATA = (
    "https://raw.githubusercontent.com/androidtrackers/"
    "certified-android-devices/master/devices.json"
)
EMOJI_PATTERN = re.compile(
    "["
    "\U0001F1E0-\U0001F1FF"  # flags (iOS)
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F680-\U0001F6FF"  # transport & map symbols
    "\U0001F700-\U0001F77F"  # alchemical symbols
    "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
    "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
    "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
    "\U0001FA00-\U0001FA6F"  # Chess Symbols
    "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
    "\U00002702-\U000027B0"  # Dingbats
    "]+"
)

CongoStr = [
    "`Congratulations and BRAVO!`",
    "`You did it! So proud of you!`",
    "`This calls for celebrating! Congratulations!`",
    "`I knew it was only a matter of time. Well done!`",
    "`Congratulations on your well-deserved success.`",
    "`Heartfelt congratulations to you.`",
    "`Warmest congratulations on your achievement.`",
    "`Congratulations and best wishes for your next adventure!”`",
    "`So pleased to see you accomplishing great things.`",
    "`Feeling so much joy for you today. What an impressive achievement!`",
]


DEL_TIME_OUT = 60
DUSER = str(ALIVE_NAME) if ALIVE_NAME else "PikaBot"
DBIO = str(AUTO_BIO) if AUTO_BIO else "Pika is Love 🔥"


def deEmojify(inputString: str) -> str:
    """Remove emojis and other non-safe characters from string"""
    return re.sub(EMOJI_PATTERN, "", inputString)


def subprocess_run(cmd):
    reply = ""
    subproc = Popen(
        cmd,
        stdout=PIPE,
        stderr=PIPE,
        shell=True,
        universal_newlines=True,
        executable="bash",
    )
    talk = subproc.communicate()
    exitCode = subproc.returncode
    if exitCode != 0:
        reply += (
            "```An error was detected while running the subprocess:\n"
            f"exit code: {exitCode}\n"
            f"stdout: {talk[0]}\n"
            f"stderr: {talk[1]}```"
        )
        return reply
    return talk


def gdrive(url: str) -> str:
    """ GDrive direct links generator """
    drive = "https://drive.google.com"
    try:
        link = re.findall(r"\bhttps?://drive\.google\.com\S+", url)[0]
    except IndexError:
        reply = "`No Google drive links found`\n"
        return reply
    file_id = ""
    reply = ""
    if link.find("view") != -1:
        file_id = link.split("/")[-2]
    elif link.find("open?id=") != -1:
        file_id = link.split("open?id=")[1].strip()
    elif link.find("uc?id=") != -1:
        file_id = link.split("uc?id=")[1].strip()
    url = f"{drive}/uc?export=download&id={file_id}"
    download = requests.get(url, stream=True, allow_redirects=False)
    cookies = download.cookies
    try:
        # In case of small file size, Google downloads directly
        dl_url = download.headers["location"]
        if "accounts.google.com" in dl_url:  # non-public file
            reply += "`Link is not public!`\n"
            return reply
        name = "Direct Download Link"
    except KeyError:
        # In case of download warning page
        page = BeautifulSoup(download.content, "lxml")
        export = drive + page.find("a", {"id": "uc-download-link"}).get("href")
        name = page.find("span", {"class": "uc-name-size"}).text
        response = requests.get(
            export, stream=True, allow_redirects=False, cookies=cookies
        )
        dl_url = response.headers["location"]
        if "accounts.google.com" in dl_url:
            reply += "Link is not public!"
            return reply
    reply += f"[{name}]({dl_url})\n"
    return reply


def zippy_share(url: str) -> str:
    """ZippyShare direct links generator
    Based on https://github.com/LameLemon/ziggy"""
    reply = ""
    dl_url = ""
    try:
        link = re.findall(r"\bhttps?://.*zippyshare\.com\S+", url)[0]
    except IndexError:
        reply = "`No ZippyShare links found`\n"
        return reply
    session = requests.Session()
    base_url = re.search("http.+.com", link).group()
    response = session.get(link)
    page_soup = BeautifulSoup(response.content, "lxml")
    scripts = page_soup.find_all("script", {"type": "text/javascript"})
    for script in scripts:
        if "getElementById('dlbutton')" in script.text:
            url_raw = re.search(
                r"= (?P<url>\".+\" \+ (?P<math>\(.+\)) .+);", script.text
            ).group("url")
            math = re.search(
                r"= (?P<url>\".+\" \+ (?P<math>\(.+\)) .+);", script.text
            ).group("math")
            dl_url = url_raw.replace(math, '"' + str(eval(math)) + '"')
            break
    dl_url = base_url + eval(dl_url)
    name = urllib.parse.unquote(dl_url.split("/")[-1])
    reply += f"[{name}]({dl_url})\n"
    return reply


def yandex_disk(url: str) -> str:
    """Yandex.Disk direct links generator
    Based on https://github.com/wldhx/yadisk-direct"""
    reply = ""
    try:
        link = re.findall(r"\bhttps?://.*yadi\.sk\S+", url)[0]
    except IndexError:
        reply = "`No Yandex.Disk links found`\n"
        return reply
    api = "https://cloud-api.yandex.net/v1/disk/public/resources/download?public_key={}"
    try:
        dl_url = requests.get(api.format(link)).json()["href"]
        name = dl_url.split("filename=")[1].split("&disposition")[0]
        reply += f"[{name}]({dl_url})\n"
    except KeyError:
        reply += "`Error: File not found / Download limit reached`\n"
        return reply
    return reply


def cm_ru(url: str) -> str:
    """cloud.mail.ru direct links generator
    Using https://github.com/JrMasterModelBuilder/cmrudl.py"""
    reply = ""
    try:
        link = re.findall(r"\bhttps?://.*cloud\.mail\.ru\S+", url)[0]
    except IndexError:
        reply = "`No cloud.mail.ru links found`\n"
        return reply
    cmd = f"bin/cmrudl -s {link}"
    result = subprocess_run(cmd)
    try:
        result = result[0].splitlines()[-1]
        data = json.loads(result)
    except json.decoder.JSONDecodeError:
        reply += "`Error: Can't extract the link`\n"
        return reply
    except IndexError:
        return reply
    dl_url = data["download"]
    name = data["file_name"]
    size = naturalsize(int(data["file_size"]))
    reply += f"[{name} ({size})]({dl_url})\n"
    return reply


def mediafire(url: str) -> str:
    """ MediaFire direct links generator """
    try:
        link = re.findall(r"\bhttps?://.*mediafire\.com\S+", url)[0]
    except IndexError:
        reply = "`No MediaFire links found`\n"
        return reply
    reply = ""
    page = BeautifulSoup(requests.get(link).content, "lxml")
    info = page.find("a", {"aria-label": "Download file"})
    dl_url = info.get("href")
    size = re.findall(r"\(.*\)", info.text)[0]
    name = page.find("div", {"class": "filename"}).text
    reply += f"[{name} {size}]({dl_url})\n"
    return reply


def sourceforge(url: str) -> str:
    """ SourceForge direct links generator """
    try:
        link = re.findall(r"\bhttps?://.*sourceforge\.net\S+", url)[0]
    except IndexError:
        reply = "`No SourceForge links found`\n"
        return reply
    file_path = re.findall(r"files(.*)/download", link)[0]
    reply = f"Mirrors for __{file_path.split('/')[-1]}__\n"
    project = re.findall(r"projects?/(.*?)/files", link)[0]
    mirrors = (
        f"https://sourceforge.net/settings/mirror_choices?"
        f"projectname={project}&filename={file_path}"
    )
    page = BeautifulSoup(requests.get(mirrors).content, "html.parser")
    info = page.find("ul", {"id": "mirrorList"}).findAll("li")
    for mirror in info[1:]:
        name = re.findall(r"\((.*)\)", mirror.text.strip())[0]
        dl_url = (
            f'https://{mirror["id"]}.dl.sourceforge.net/project/{project}/{file_path}'
        )
        reply += f"[{name}]({dl_url}) "
    return reply


def osdn(url: str) -> str:
    """ OSDN direct links generator """
    osdn_link = "https://osdn.net"
    try:
        link = re.findall(r"\bhttps?://.*osdn\.net\S+", url)[0]
    except IndexError:
        reply = "`No OSDN links found`\n"
        return reply
    page = BeautifulSoup(
        requests.get(
            link,
            allow_redirects=True).content,
        "lxml")
    info = page.find("a", {"class": "mirror_link"})
    link = urllib.parse.unquote(osdn_link + info["href"])
    reply = f"Mirrors for __{link.split('/')[-1]}__\n"
    mirrors = page.find("form", {"id": "mirror-select-form"}).findAll("tr")
    for data in mirrors[1:]:
        mirror = data.find("input")["value"]
        name = re.findall(r"\((.*)\)", data.findAll("td")[-1].text.strip())[0]
        dl_url = re.sub(r"m=(.*)&f", f"m={mirror}&f", link)
        reply += f"[{name}]({dl_url}) "
    return reply


def androidfilehost(url: str) -> str:
    """ AFH direct links generator """
    try:
        link = re.findall(r"\bhttps?://.*androidfilehost.*fid.*\S+", url)[0]
    except IndexError:
        reply = "`No AFH links found`\n"
        return reply
    fid = re.findall(r"\?fid=(.*)", link)[0]
    session = requests.Session()
    user_agent = useragent()
    headers = {"user-agent": user_agent}
    res = session.get(link, headers=headers, allow_redirects=True)
    headers = {
        "origin": "https://androidfilehost.com",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9",
        "user-agent": user_agent,
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "x-mod-sbb-ctype": "xhr",
        "accept": "*/*",
        "referer": f"https://androidfilehost.com/?fid={fid}",
        "authority": "androidfilehost.com",
        "x-requested-with": "XMLHttpRequest",
    }
    data = {
        "submit": "submit",
        "action": "getdownloadmirrors",
        "fid": f"{fid}"}
    mirrors = None
    reply = ""
    error = "`Error: Can't find Mirrors for the link`\n"
    try:
        req = session.post(
            "https://androidfilehost.com/libs/otf/mirrors.otf.php",
            headers=headers,
            data=data,
            cookies=res.cookies,
        )
        mirrors = req.json()["MIRRORS"]
    except (json.decoder.JSONDecodeError, TypeError):
        reply += error
    if not mirrors:
        reply += error
        return reply
    for item in mirrors:
        name = item["name"]
        dl_url = item["url"]
        reply += f"[{name}]({dl_url}) "
    return reply


def useragent():
    """
    useragent random setter
    """
    useragents = BeautifulSoup(
        requests.get(
            "https://developers.whatismybrowser.com/"
            "useragents/explore/operating_system_name/android/"
        ).content,
        "lxml",
    ).findAll("td", {"class": "useragent"})
    user_agent = choice(useragents)
    return user_agent.text


async def pbio(event):
    if event.fwd_from:
        return
    bio = event.pattern_match.group(1)
    try:
        await event.client(functions.account.UpdateProfileRequest(about=bio))
        await event.edit("Succesfully changed my profile bio")
    except Exception as e:
        await event.edit(str(e))


async def pname(event):
    if event.fwd_from:
        return
    names = event.pattern_match.group(1)
    first_name = names
    last_name = ""
    if "\\n" in names:
        first_name, last_name = names.split("\\n", 1)
    try:
        await event.client(
            functions.account.UpdateProfileRequest(
                first_name=first_name, last_name=last_name
            )
        )
        await event.edit("My name was changed successfully")
    except Exception as e:
        await event.edit(str(e))


async def anpfp(event):
    await event.edit(f"{r}")
    while True:
        await animepp()
        file = await event.client.upload_file("donottouch.jpg")
        await event.client(functions.photos.UploadProfilePhotoRequest(file))
        os.system("rm -rf donottouch.jpg")
        await asyncio.sleep(60)


async def avpfp(event):
    await event.edit(f"{s}")
    while True:
        await avengerspic()
        file = await event.client.upload_file("donottouch.jpg")
        await event.client(functions.photos.UploadProfilePhotoRequest(file))
        os.system("rm -rf donottouch.jpg")
        await asyncio.sleep(600)


async def gmpfp(event):
    await event.edit(f"{t}")
    while True:
        await gamerpic()
        file = await event.client.upload_file("donottouch.jpg")
        await event.client(functions.photos.UploadProfilePhotoRequest(file))
        os.system("rm -rf donottouch.jpg")
        await asyncio.sleep(60)


async def atnm(event):
    if event.fwd_from:
        return
    while True:
        dname = await pikaa(event, "ALIVE_NAME")
        DM = time.strftime("%d-%m-%y")
        HM = time.strftime("%H:%M")
        name = f"🕒{HM} ⚡{dname}⚡ 📅{DM}"
        pikalog.info(name)
        try:
            await event.client(functions.account.UpdateProfileRequest(first_name=name))
        except FloodWaitError as ex:
            logger.warning(str(e))
            await asyncio.sleep(ex.seconds)
        await asyncio.sleep(DEL_TIME_OUT)
    await event.edit(f"Auto Name has been started Master")


async def atb(event):
    if event.fwd_from:
        return
    while True:
        DMY = time.strftime("%d.%m.%Y")
        HM = time.strftime("%H:%M:%S")
        bio = f"📅 {DMY} | {DBIO} | ⌚️ {HM}"
        pikalog.info(bio)
        try:
            await event.client(functions.account.UpdateProfileRequest(about=bio))
        except FloodWaitError as ex:
            logger.warning(str(e))
            await asyncio.sleep(ex.seconds)
        await asyncio.sleep(DEL_TIME_OUT)


async def _setgpic(gpic):
    """ For .setgpic command, changes the picture of a group """
    if not gpic.is_group:
        await gpic.edit("`I don't think this is a group.`")
        return
    replymsg = await gpic.get_reply_message()
    chat = await gpic.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    photo = None

    if not admin and not creator:
        await gpic.edit(NO_ADMIN)
        return

    if replymsg and replymsg.media:
        if isinstance(replymsg.media, MessageMediaPhoto):
            photo = await gpic.client.download_media(message=replymsg.photo)
        elif "image" in replymsg.media.document.mime_type.split("/"):
            photo = await gpic.client.download_file(replymsg.media.document)
        else:
            await gpic.edit(INVALID_MEDIA)

    if photo:
        try:
            await gpic.client(
                EditPhotoRequest(gpic.chat_id, await gpic.client.upload_file(photo))
            )
            await gpic.edit(CHAT_PP_CHANGED)

        except PhotoCropSizeSmallError:
            await gpic.edit(PP_TOO_SMOL)
        except ImageProcessFailedError:
            await gpic.edit(PP_ERROR)


async def _promote(promt):
    """ For .promote command, promotes the replied/tagged person """
    # Get targeted chat
    chat = await promt.get_chat()
    # Grab admin status or creator in a chat
    admin = chat.admin_rights
    creator = chat.creator

    # If not admin and not creator, also return
    if not admin and not creator:
        await promt.edit(NO_ADMIN)
        return

    new_rights = ChatAdminRights(
        add_admins=False,
        invite_users=True,
        change_info=False,
        ban_users=True,
        delete_messages=True,
        pin_messages=True,
    )
    _tg = await get_pika_tg(promt)
    a = await pika_msg(promt, "`Promoting...`", _tg)
    user, rank = await get_user_from_event(promt)
    if not rank:
        # Just in case.
        rank = "admeme"
    if user:
        pass
    else:
        return

    # Try to promote if current user is admin or creator
    try:
        await promt.client(EditAdminRequest(promt.chat_id, user.id, new_rights, rank))
        await pika_msg(a, "`Promoted Successfully!`")

    # If Telethon spit BadRequestError, assume
    # we don't have Promote permission
    except BadRequestError:
        await pika_msg(a, NO_PERM)
        return

    # Announce to the logging group if we have promoted successfully
    if BOTLOG:
        await promt.client.send_message(
            BOTLOG_CHATID,
            "#PROMOTE\n"
            f"USER: [{user.first_name}](tg://user?id={user.id})\n"
            f"CHAT: {promt.chat.title}(`{promt.chat_id}`)",
        )


async def _demote(dmod):
    """ For .demote command, demotes the replied/tagged person """
    # Admin right check
    chat = await dmod.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    if not admin and not creator:
        await dmod.edit(NO_ADMIN)
        return

    # If passing, declare that we're going to demote
    _tg = await get_pika_tg(dmod)
    a = await pika_msg(dmod, _tg, "`Demoting...`")
    rank = "admeme"  # dummy rank, lol.
    user = await get_user_from_event(dmod)
    user = user[0]
    if user:
        pass
    else:
        return

    # New rights after demotion
    newrights = ChatAdminRights(
        add_admins=None,
        invite_users=None,
        change_info=None,
        ban_users=None,
        delete_messages=None,
        pin_messages=None,
    )
    # Edit Admin Permission
    try:
        await dmod.client(EditAdminRequest(dmod.chat_id, user.id, newrights, rank))

    # If we catch BadRequestError from Telethon
    # Assume we don't have permission to demote
    except BadRequestError:
        await pika_msg(a, NO_PERM)
        return
    await pika_msg(a, "`Demoted Successfully!`")

    # Announce to the logging group if we have demoted successfully
    if BOTLOG:
        await dmod.client.send_message(
            BOTLOG_CHATID,
            "#DEMOTE\n"
            f"USER: [{user.first_name}](tg://user?id={user.id})\n"
            f"CHAT: {dmod.chat.title}(`{dmod.chat_id}`)",
        )


async def _ban(bon):
    """ For .ban command, bans the replied/tagged person """
    # Here laying the sanity check
    chat = await bon.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # Well
    if not admin and not creator:
        await bon.edit(NO_ADMIN)
        return

    user, reason = await get_user_from_event(bon)
    if user:
        pass
    else:
        return
    _tg = await get_pika_tg(bon)
    # Announce that we're going to whack the pest
    a = await pika_msg(
        bon,
        "`Whacking the pest!`",
        _tg,
    )

    try:
        await bon.client(EditBannedRequest(bon.chat_id, user.id, BANNED_RIGHTS))
    except BadRequestError:
        await pika_msg(a, NO_PERM)
        return
    # Helps ban group join spammers more easily
    try:
        reply = await bon.get_reply_message()
        if reply:
            await reply.delete()
    except BadRequestError:
        await pika_msg(
            a, "`I dont have message nuking rights! But still he was banned!`"
        )
        return
    # Delete message and then tell that the command
    # is done gracefully
    # Shout out the ID, so that fedadmins can fban later
    if reason:
        await pika_msg(
            a,
            f"{user.first_name} was banned !!\
        \nID: `{str(user.id)}`\
        \nReason: {reason}",
        )
    else:
        await pika_msg(
            a,
            f"{user.first_name} was banned !!\
        \nID: `{str(user.id)}`",
        )
    # Announce to the logging group if we have banned the person
    # successfully!
    if BOTLOG:
        await bon.client.send_message(
            BOTLOG_CHATID,
            "#BAN\n"
            f"USER: [{user.first_name}](tg://user?id={user.id})\n"
            f"CHAT: {bon.chat.title}(`{bon.chat_id}`)",
        )


async def _unban(unbon):
    """ For .unban command, unbans the replied/tagged person """
    # Here laying the sanity check
    chat = await unbon.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # Well
    if not admin and not creator:
        await unbon.edit(NO_ADMIN)
        return

    # If everything goes well...
    _tg = await get_pika_tg(unbon)
    a = await pika_msg(unbon, "`Unbanning...`", _tg)

    user = await get_user_from_event(unbon)
    user = user[0]
    if user:
        pass
    else:
        return

    try:
        await unbon.client(EditBannedRequest(unbon.chat_id, user.id, UNBAN_RIGHTS))
        await pika_msg(a, "```Unbanned Successfully```")

        if BOTLOG:
            await unbon.client.send_message(
                BOTLOG_CHATID,
                "#UNBAN\n"
                f"USER: [{user.first_name}](tg://user?id={user.id})\n"
                f"CHAT: {unbon.chat.title}(`{unbon.chat_id}`)",
            )
    except UserIdInvalidError:
        await pika_msg(a, "`Uh oh my unban logic broke!`")


async def _mute(spdr):
    """
    This function is basically muting peeps
    """
    # Check if the function running under SQL mo
    try:
        from pikabot.sql_helper.mute_sql import mute
    except AttributeError:
        await spdr.edit(NO_SQL)
        return

    # Admin or creator check
    chat = await spdr.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # If not admin and not creator, return
    if not admin and not creator:
        await spdr.edit(NO_ADMIN)
        return

    user, reason = await get_user_from_event(spdr)
    if user:
        pass
    else:
        return

    _tg = await get_pika_tg(spdr)
    self_user = await get_pika_id(spdr)

    if user.id == self_user:
        await pika_msg(
            spdr, "`Hands too short, can't duct tape myself...\n(ヘ･_･)ヘ┳━┳`", _tg
        )
        return

    # If everything goes well, do announcing and mute
    a = await pika_msg(spdr, _tg, "`Muting...`")
    pikamute = mute(spdr.chat_id, user.id, self_user)
    if pikamute is False:
        return await spdr.edit("`Error! User probably already muted.`")
    else:
        try:
            await spdr.client(EditBannedRequest(spdr.chat_id, user.id, MUTE_RIGHTS))

            # Announce that the function is done
            if reason:
                await pika_msg(a, f"`Safely taped !!`\nReason: {reason}")
            else:
                await pika_msg(a, "`Safely taped !!`")

            # Announce to logging group
            if BOTLOG:
                await spdr.client.send_message(
                    BOTLOG_CHATID,
                    "#MUTE\n"
                    f"USER: [{user.first_name}](tg://user?id={user.id})\n"
                    f"CHAT: {spdr.chat.title}(`{spdr.chat_id}`)",
                )
        except UserIdInvalidError:
            return await pika_msg(a, "`Uh oh my mute logic broke!`")


async def _unmute(unmot):
    """ For .unmute command, unmute the replied/tagged person """
    # Admin or creator check
    await unmot.client.get_me()
    chat = await unmot.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # If not admin and not creator, return
    if not admin and not creator:
        await unmot.edit(NO_ADMIN)
        return

    # Check if the function running under SQL mode
    try:
        from pikabot.sql_helper.mute_sql import unmute
    except AttributeError:
        await unmot.edit(NO_SQL)
        return

    # If admin or creator, inform the user and start unmuting
    pika_id = await get_pika_id(unmot)
    _tg = await get_pika_tg(unmot)
    a = await pika_msg(unmot, "```Unmuting...```", _tg)
    user = await get_user_from_event(unmot)
    user = user[0]
    if user:
        pass
    else:
        return

    pikaumute = unmute(unmot.chat_id, user.id, pika_id)
    if pikaumute is False:
        return await pika_msg(a, "`Error! User probably already unmuted.`")
    else:

        try:
            await unmot.client(EditBannedRequest(unmot.chat_id, user.id, UNBAN_RIGHTS))
            await pika_msg(a, "```Unmuted Successfully```")
        except UserIdInvalidError:
            await pika_msg(a, "`Uh oh my unmute logic broke!`")
            return

        if BOTLOG:
            await unmot.client.send_message(
                BOTLOG_CHATID,
                "#UNMUTE\n"
                f"USER: [{user.first_name}](tg://user?id={user.id})\n"
                f"CHAT: {unmot.chat.title}(`{unmot.chat_id}`)",
            )


async def _ungmute(un_gmute):
    """ For .ungmute command, ungmutes the target in the userbot """
    # Admin or creator check
    await un_gmute.client.get_me()
    _tg = await get_pika_tg(un_gmute)
    _pika_id = await get_pika_id(un_gmute)
    chat = await un_gmute.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # If not admin and not creator, return
    if not admin and not creator:
        await un_gmute.edit(NO_ADMIN)
        return

    # Check if the function running under SQL mode
    try:
        from pikabot.sql_helper.gmute_sql import ungmute
    except AttributeError:
        await un_gmute.edit(NO_SQL)
        return

    user = await get_user_from_event(un_gmute)
    user = user[0]
    if user:
        pass
    else:
        return

    # If pass, inform and start ungmuting
    a = await pika_msg(un_gmute, "```Ungmuting...```", _tg)

    pikaugmute = ungmute(user.id, _pika_id)
    if pikaugmute is False:
        await pika_msg(a, "`Error! User probably not gmuted.`")
    else:
        b = 0
        if await is_pikatg(un_gmute):
            from pikabot.sql_helper.chats_sql import (
                get_pika_chats,
            )

            id = get_pika_chats()
            for _umte in id:
                try:
                    b += 1
                    await un_gmute.client(
                        EditBannedRequest(
                            int(_umte.pika_id), int(user.id), UNMUTE_RIGHTS
                        )
                    )
                    await pika_msg(a, f"Globally UnMuting in {b} Chats")
                except BaseException:
                    pass
        else:
            async for ugmte in un_gmute.client.iter_dialogs():
                if ugmte.is_group or ugmte.is_channel:
                    ugchat = ugmte.id
                    try:
                        b += 1
                        await un_gmute.client(
                            EditBannedRequest(ugchat, user.id, UNMUTE_RIGHTS)
                        )
                        await pika_msg(a, f"Globally UnMuting in {b} Chats")
                    except BaseException:
                        pass
        await pika_msg(a, f"**Globally UnMuted User in {b} Chats**")
        if BOTLOG:
            await un_gmute.client.send_message(
                BOTLOG_CHATID,
                "#UNGMUTE\n"
                f"USER: [{user.first_name}](tg://user?id={user.id})\n"
                f"CHAT: {un_gmute.chat.title}(`{un_gmute.chat_id}`)",
            )


async def _gmte(gspdr):
    """ For .gmute command, globally mutes the replied/tagged person """
    # Admin or creator check
    await gspdr.client.get_me()
    _pika_id = await get_pika_id(gspdr)
    _tg = await get_pika_tg(gspdr)
    chat = await gspdr.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # If not admin and not creator, return
    if not admin and not creator:
        await gspdr.edit(NO_ADMIN)
        return

    # Check if the function running under SQL mode
    try:
        from pikabot.sql_helper.gmute_sql import gmute
    except AttributeError:
        await gspdr.edit(NO_SQL)
        return

    user, reason = await get_user_from_event(gspdr)
    if user:
        pass
    else:
        return

    # If pass, inform and start gmuting
    a = await pika_msg(gspdr, "`Grabs a huge, sticky duct tape!`", _tg)

    pikagmute = gmute(user.id, _pika_id)
    if pikagmute is False:
        await pika_msg(a, "`Error! User probably already gmuted.\nRe-rolls the tape.`")
    else:
        if reason:
            await pika_msg(a, f"`Globally taped!`Reason: {reason}")
        else:
            await pika_msg(a, "`Globally taped!`")

        if BOTLOG:
            await gspdr.client.send_message(
                BOTLOG_CHATID,
                "#GMUTE\n"
                f"USER: [{user.first_name}](tg://user?id={user.id})\n"
                f"CHAT: {gspdr.chat.title}(`{gspdr.chat_id}`)",
            )


async def _rmdacc(show):
    """ For .delusers command, list all the ghost/deleted accounts in a chat. """
    _tg = await get_pika_tg(show)
    if not show.is_group:
        await pika_msg(show, "`I don't think this is a group.`", _tg)
        return
    con = show.pattern_match.group(1)
    del_u = 0
    del_status = "`No deleted accounts found, Group is cleaned as Hell`"

    if con != "clean":
        a = await pika_msg(show, "`Searching for zombie accounts...`", _tg)
        async for user in show.client.iter_participants(show.chat_id, aggressive=True):
            if user.deleted:
                del_u += 1
                await sleep(1)
        if del_u > 0:
            del_status = f"Found **{del_u}** deleted account(s) in this group,\
            \nclean them by using .delusers clean"

        a = await pika_msg(show, del_status)
        return

    # Here laying the sanity check
    chat = await show.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # Well
    if not admin and not creator:
        await pika_msg(a, "`I am not an admin here!`")
        return

    await pika_msg(a, "`Deleting deleted accounts...\nOh I can do that?!?!`")
    del_u = 0
    del_a = 0

    async for user in show.client.iter_participants(show.chat_id):
        if user.deleted:
            try:
                await show.client(
                    EditBannedRequest(show.chat_id, user.id, BANNED_RIGHTS)
                )
            except ChatAdminRequiredError:
                await pika_msg(a, "`I don't have ban rights in this group`")
                return
            except UserAdminInvalidError:
                del_u -= 1
                del_a += 1
            await show.client(EditBannedRequest(show.chat_id, user.id, UNBAN_RIGHTS))
            del_u += 1

    if del_u > 0:
        del_status = f"Cleaned **{del_u}** deleted account(s)"

    if del_a > 0:
        del_status = f"Cleaned **{del_u}** deleted account(s) \
        \n**{del_a}** deleted admin accounts are not removed"

    await pika_msg(a, del_status)
    await sleep(2)
    await show.delete()

    if BOTLOG:
        await show.client.send_message(
            BOTLOG_CHATID,
            "#CLEANUP\n"
            f"Cleaned **{del_u}** deleted account(s) !!\
            \nCHAT: {show.chat.title}(`{show.chat_id}`)",
        )


async def _gadmin(show):
    """ For .admins command, list all of the admins of the chat. """
    info = await show.client.get_entity(show.chat_id)
    title = info.title if info.title else "this chat"
    _tg = await get_pika_tg(show)
    a = await pika_msg(show, "Getting admins, please wait...", _tg)
    mentions = f"<b>Admins in {title}:</b> \n"
    try:
        async for user in show.client.iter_participants(
            show.chat_id, filter=ChannelParticipantsAdmins
        ):
            if not user.deleted:
                link = f'<a href="tg://user?id={user.id}">{user.first_name}</a>'
                userid = f"<code>{user.id}</code>"
                mentions += f"\n{link} {userid}"
            else:
                mentions += f"\nDeleted Account <code>{user.id}</code>"
    except ChatAdminRequiredError as err:
        mentions += " " + str(err) + "\n"
    await pika_msg(a, mentions, parse_mode="html")


async def _pin(msg):
    """ For .pin command, pins the replied/tagged message on the top the chat. """
    # Admin or creator check
    chat = await msg.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # If not admin and not creator, return
    if not admin and not creator:
        await msg.edit(NO_ADMIN)
        return
    _tg = await get_pika_tg(msg)
    to_pin = msg.reply_to_msg_id

    if not to_pin:
        await pika_msg(msg, "`Reply to a message to pin it.`", _tg)
        return

    options = msg.pattern_match.group(1)

    is_silent = True

    if options.lower() == "loud":
        is_silent = False

    try:
        await msg.client(UpdatePinnedMessageRequest(msg.to_id, to_pin, is_silent))
    except BadRequestError:
        await pika_msg(msg, NO_PERM, _tg)
        return

    await pika_msg(msg, "`Pinned Successfully!`")

    user = await get_user_sender_id(msg.sender_id, msg)

    if BOTLOG:
        await msg.client.send_message(
            BOTLOG_CHATID,
            "#PIN\n"
            f"ADMIN: [{user.first_name}](tg://user?id={user.id})\n"
            f"CHAT: {msg.chat.title}(`{msg.chat_id}`)\n"
            f"LOUD: {not is_silent}",
        )


async def _kick(usr):
    """ For .kick command, kicks the replied/tagged person from the group. """
    # Admin or creator check
    _tg = await get_pika_tg(usr)
    chat = await usr.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # If not admin and not creator, return
    if not admin and not creator:
        await usr.edit(NO_ADMIN, _tg)
        return

    user, reason = await get_user_from_event(usr)
    if not user:
        await pika_msg(usr, "`Couldn't fetch user.`", _tg)
        return

    a = await pika_msg(usr, "`Kicking...`", _tg)

    try:
        await usr.client.kick_participant(usr.chat_id, user.id)
        await sleep(0.5)
    except Exception as e:
        await pika_msg(a, NO_PERM + f"\n{str(e)}")
        return

    if reason:
        await pika_msg(
            a,
            f"`Kicked` [{user.first_name}](tg://user?id={user.id})`!`\nReason: {reason}",
        )
    else:
        await pika_msg(a, f"`Kicked` [{user.first_name}](tg://user?id={user.id})`!`")

    if BOTLOG:
        await usr.client.send_message(
            BOTLOG_CHATID,
            "#KICK\n"
            f"USER: [{user.first_name}](tg://user?id={user.id})\n"
            f"CHAT: {usr.chat.title}(`{usr.chat_id}`)\n",
        )


async def _gusers(show):
    """ For .users command, list all of the users in a chat. """
    info = await show.client.get_entity(show.chat_id)
    title = info.title if info.title else "this chat"
    mentions = "Users in {}: \n".format(title)
    try:
        if not show.pattern_match.group(1):
            async for user in show.client.iter_participants(show.chat_id):
                if not user.deleted:
                    mentions += (
                        f"\n[{user.first_name}](tg://user?id={user.id}) `{user.id}`"
                    )
                else:
                    mentions += f"\nDeleted Account `{user.id}`"
        else:
            searchq = show.pattern_match.group(1)
            async for user in show.client.iter_participants(
                show.chat_id, search=f"{searchq}"
            ):
                if not user.deleted:
                    mentions += (
                        f"\n[{user.first_name}](tg://user?id={user.id}) `{user.id}`"
                    )
                else:
                    mentions += f"\nDeleted Account `{user.id}`"
    except ChatAdminRequiredError as err:
        mentions += " " + str(err) + "\n"
    try:
        await show.edit(mentions)
    except MessageTooLongError:
        await show.edit("Damn, this is a huge group. Uploading users lists as file.")
        file = open("userslist.txt", "w+")
        file.write(mentions)
        file.close()
        await show.client.send_file(
            show.chat_id,
            "userslist.txt",
            caption="Users in {}".format(title),
            reply_to=show.id,
        )
        remove("userslist.txt")


async def _muter(moot):
    try:
        from pikabot.sql_helper.gmute_sql import is_gmuted
    except AttributeError:
        return
    _pika_id = await get_pika_id(moot)
    gmuted = is_gmuted(moot.sender_id)
    rights = ChatBannedRights(
        until_date=None,
        send_messages=True,
        send_media=True,
        send_stickers=True,
        send_gifs=True,
        send_games=True,
        send_inline=True,
        embed_links=True,
    )

    if not moot.is_private:
        for i in gmuted:
            if i.sender == str(moot.sender_id) and i.pika_id == _pika_id:
                try:
                    await moot.client(
                        EditBannedRequest(moot.chat_id, moot.sender_id, MUTE_RIGHTS)
                    )
                except BadRequestError:
                    return
                await moot.reply(
                    "Globally Muted User Detected : **MUTED SUCCESSFULLY**"
                )

    if moot.is_private:
        for i in gmuted:
            if i.sender == str(moot.sender_id) and i.pika_id == _pika_id:
                await moot.delete()


async def gban(event):
    if event.fwd_from:
        return
    _tg = await get_pika_tg(event)
    pika_id = await get_pika_id(event)
    st = pikatime.now()
    a = await pika_msg(event, "**GBanning This User !**", _tg)
    suc = 0
    bd = 0

    user, reason = await get_user_from_event(event)
    if not user:
        await pika_msg(a, "Kindly, Mention A User To Gban")
        return
    if not reason or reason is None:
        rson = "#GBanned"
    elif reason:
        rson = reason
    if user.id == bot.uid:
        await pika_msg(a, "**I Can't Gban You Master ☹️**")
        return
    if gban_sql.is_gbanned(user.id, pika_id):
        await pika_msg(a, "**This User Is Already Gbanned.**")
        return

    gban_sql.gban(user.id, pika_id, rson)
    await pika_msg(a, f"**Trying To GBan [{user.first_name}](tg://user?id={user.id})**")
    async for pik in event.client.iter_dialogs():
        if pik.is_group or pik.is_channel:
            try:
                await event.client.edit_permissions(
                    pik.id, user.id, view_messages=False
                )
                suc += 1
            except BaseException:
                bd += 0
    et = pikatime.now()
    tott = round(et - st)
    await pika_msg(
        a,
        f"**GBanned Successfully !** \n\n"
        f"**User :** [{user.first_name}](tg://user?id={user.id}) \n"
        f"**Affected Chats :** {suc} \n"
        f"**Due to :** {rson} \n"
        f"**Time Taken :** {tott} \n"
        f"[{user.first_name}](tg://user?id={user.id}) Will be banned whenever he/she will join any group where you are admin",
    )


async def _allnotes(event):
    if event.fwd_from:
        return
    _tg = await get_pika_tg(event)
    _pika_id = await get_pika_id(event)
    message = "`There are no saved notes in this chat`"
    notes = get_notes(event.chat_id, _pika_id)
    for note in notes:
        if message == "`There are no saved notes in this chat`":
            message = "Notes saved in this chat:\n"
            message += "`#{}`\n".format(note.keyword)
        else:
            message += "`#{}`\n".format(note.keyword)
    await pika_msg(event, message, _tg)


async def _remove_notes(event):
    if event.fwd_from:
        return
    _tg = await get_pika_tg(event)
    _pika_id = await get_pika_id(event)
    notename = event.pattern_match.group(1)
    if rm_note(event.chat_id, notename, _pika_id) is False:
        return await pika_msg(
            event, "`Couldn't find note:` **{}**".format(notename), _tg
        )
    else:
        return await pika_msg(
            event, "`Successfully deleted note:` **{}**".format(notename), _tg
        )


async def _add_notes(event):
    if event.fwd_from:
        return
    _tg = await get_pika_tg(event)
    client_id = await get_pika_id(event)
    keyword = event.pattern_match.group(1)
    string = event.text.partition(keyword)[2]
    msg = await event.get_reply_message()
    msg_id = None
    if msg and msg.media and not string:
        if BOTLOG_CHATID:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"#NOTE\
            \nCHAT ID: {event.chat_id}\
            \nKEYWORD: {keyword}\
            \n\nThe following message is saved as the note's reply data for the chat, please do NOT delete it !!",
            )
            msg_o = await event.client.forward_messages(
                entity=BOTLOG_CHATID, messages=msg, from_peer=event.chat_id, silent=True
            )
            msg_id = msg_o.id
        else:
            await pika_msg(
                event,
                "Saving media as data for the note requires the BOTLOG_CHATID to be set.",
                _tg,
            )
            return
    elif event.reply_to_msg_id and not string:
        rep_msg = await event.get_reply_message()
        string = rep_msg.text
    success = "Note {} successfully. Use #{} to get it"
    if add_note(str(event.chat_id), keyword,
                string, msg_id, client_id) is False:
        return await pika_msg(event, success.format("updated", keyword), _tg)
    else:
        return await pika_msg(event, success.format("added", keyword), _tg)


async def note_incm(getnt):
    try:
        _pika_id = await get_pika_id(getnt)
        if not (await getnt.get_sender()).bot:
            notename = getnt.text[1:]
            note = get_note(getnt.chat_id, notename, _pika_id)
            message_id_to_reply = getnt.message.id
            if not message_id_to_reply:
                message_id_to_reply = None
            if note and note.f_mesg_id:
                msg_o = await getnt.client.get_messages(
                    entity=BOTLOG_CHATID, ids=int(note.f_mesg_id)
                )
                await getnt.client.send_message(
                    getnt.chat_id,
                    msg_o.message,
                    reply_to=message_id_to_reply,
                    file=msg_o.media,
                )
            elif note and note.reply:
                await getnt.client.send_message(
                    getnt.chat_id,
                    note.reply,
                    reply_to=message_id_to_reply,
                    link_preview=False,
                )
    except AttributeError:
        pass


async def get_user_from_event(event):
    """ Get the user from argument or replied message. """
    args = event.pattern_match.group(1).split(" ", 1)
    extra = None
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        user_obj = await event.client.get_entity(previous_message.sender_id)
        extra = event.pattern_match.group(1)
    elif args:
        user = args[0]
        if len(args) == 2:
            extra = args[1]

        if user.isnumeric():
            user = int(user)

        if not user:
            await event.edit("`Pass the user's username, id or reply!`")
            return

        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]

            if isinstance(
                    probable_user_mention_entity,
                    MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await event.client.get_entity(user_id)
                return user_obj
        try:
            user_obj = await event.client.get_entity(user)
        except (TypeError, ValueError) as err:
            await event.edit(str(err))
            return None

    return user_obj, extra


async def get_user_sender_id(user, event):
    if isinstance(user, str):
        user = int(user)

    try:
        user_obj = await event.client.get_entity(user)
    except (TypeError, ValueError) as err:
        await event.edit(str(err))
        return None

    return user_obj


async def _alive(event):
    pupt = grt((time.time() - UpTime))
    try:
        pic = await pikaa(event, "ALIVE_PIC")
    except BaseException:
        pic = apic
    az = await pikaa(event, "ALIVE_NAME")
    await event.delete()
    a = await event.client.send_file(
        event.chat_id, pic, caption=alivestr.format(pupt, az)
    )
    await asyncio.sleep(30)
    await a.delete()


async def magisk(request):
    """ magisk latest releases """
    magisk_dict = {
        "Stable": "https://raw.githubusercontent.com/topjohnwu/magisk_files/master/stable.json",
        "Beta": "https://raw.githubusercontent.com/topjohnwu/magisk_files/master/beta.json",
        "Canary (Release)": "https://raw.githubusercontent.com/topjohnwu/magisk_files/canary/release.json",
        "Canary (Debug)": "https://raw.githubusercontent.com/topjohnwu/magisk_files/canary/debug.json",
    }
    releases = "Latest Magisk Releases:\n"
    for name, release_url in magisk_dict.items():
        data = get(release_url).json()
        releases += (
            f'{name}: [ZIP v{data["magisk"]["version"]}]({data["magisk"]["link"]}) | '
            f'[APK v{data["app"]["version"]}]({data["app"]["link"]}) | '
            f'[Uninstaller]({data["uninstaller"]["link"]})\n')
    await request.edit(releases)


async def device_info(request):
    """ get android device basic info from its codename """
    textx = await request.get_reply_message()
    device = request.pattern_match.group(1)
    if device:
        pass
    elif textx:
        device = textx.text
    else:
        await request.edit("`Usage: .device <codename> / <model>`")
        return
    found = [
        i
        for i in get(DEVICES_DATA).json()
        if i["device"] == device or i["model"] == device
    ]
    if found:
        reply = f"Search results for {device}:\n\n"
        for item in found:
            brand = item["brand"]
            name = item["name"]
            codename = item["device"]
            model = item["model"]
            reply += (
                f"{brand} {name}\n"
                f"**Codename**: `{codename}`\n"
                f"**Model**: {model}\n\n"
            )
    else:
        reply = f"`Couldn't find info about {device}!`\n"
    await request.edit(reply)


async def codename_info(request):
    """ search for android codename """
    textx = await request.get_reply_message()
    brand = request.pattern_match.group(1).lower()
    device = request.pattern_match.group(2).lower()
    if brand and device:
        pass
    elif textx:
        brand = textx.text.split(" ")[0]
        device = " ".join(textx.text.split(" ")[1:])
    else:
        await request.edit("`Usage: .codename <brand> <device>`")
        return
    found = [
        i
        for i in get(DEVICES_DATA).json()
        if i["brand"].lower() == brand and device in i["name"].lower()
    ]
    if len(found) > 8:
        found = found[:8]
    if found:
        reply = f"Search results for {brand.capitalize()} {device.capitalize()}:\n\n"
        for item in found:
            brand = item["brand"]
            name = item["name"]
            codename = item["device"]
            model = item["model"]
            reply += (
                f"{brand} {name}\n"
                f"**Codename**: `{codename}`\n"
                f"**Model**: {model}\n\n"
            )
    else:
        reply = f"`Couldn't find {device} codename!`\n"
    await request.edit(reply)


async def dspecs(request):
    """ Mobile devices specifications """
    textx = await request.get_reply_message()
    brand = request.pattern_match.group(1).lower()
    device = request.pattern_match.group(2).lower()
    if brand and device:
        pass
    elif textx:
        brand = textx.text.split(" ")[0]
        device = " ".join(textx.text.split(" ")[1:])
    else:
        await request.edit("`Usage: .specs <brand> <device>`")
        return
    all_brands = (
        BeautifulSoup(
            get("https://www.devicespecifications.com/en/brand-more").content,
            "lxml") .find(
            "div",
            {
                "class": "brand-listing-container-news"}) .findAll("a"))
    brand_page_url = None
    try:
        brand_page_url = [
            i["href"] for i in all_brands if brand == i.text.strip().lower()
        ][0]
    except IndexError:
        await request.edit(f"`{brand} is unknown brand!`")
    devices = BeautifulSoup(get(brand_page_url).content, "lxml").findAll(
        "div", {"class": "model-listing-container-80"}
    )
    device_page_url = None
    try:
        device_page_url = [
            i.a["href"]
            for i in BeautifulSoup(str(devices), "lxml").findAll("h3")
            if device in i.text.strip().lower()
        ]
    except IndexError:
        await request.edit(f"`can't find {device}!`")
    if len(device_page_url) > 2:
        device_page_url = device_page_url[:2]
    reply = ""
    for url in device_page_url:
        info = BeautifulSoup(get(url).content, "lxml")
        reply = "\n**" + info.title.text.split("-")[0].strip() + "**\n\n"
        info = info.find("div", {"id": "model-brief-specifications"})
        specifications = re.findall(r"<b>.*?<br/>", str(info))
        for item in specifications:
            title = re.findall(r"<b>(.*?)</b>", item)[0].strip()
            data = (
                re.findall(r"</b>: (.*?)<br/>", item)[0]
                .replace("<b>", "")
                .replace("</b>", "")
                .strip()
            )
            reply += f"**{title}**: {data}\n"
    await request.edit(reply)


async def twrp(request):
    """ get android device twrp """
    textx = await request.get_reply_message()
    device = request.pattern_match.group(1)
    if device:
        pass
    elif textx:
        device = textx.text.split(" ")[0]
    else:
        await request.edit("`Usage: .twrp <codename>`")
        return
    url = get(f"https://dl.twrp.me/{device}/")
    if url.status_code == 404:
        reply = f"`Couldn't find twrp downloads for {device}!`\n"
        await request.edit(reply)
        return
    page = BeautifulSoup(url.content, "lxml")
    download = page.find("table").find("tr").find("a")
    dl_link = f"https://dl.twrp.me{download['href']}"
    dl_file = download.text
    size = page.find("span", {"class": "filesize"}).text
    date = page.find("em").text.strip()
    reply = (
        f"**Latest TWRP for {device}:**\n"
        f"[{dl_file}]({dl_link}) - __{size}__\n"
        f"**Updated:** __{date}__\n"
    )
    await request.edit(reply)


async def waifu(animu):
    # """Creates random anime sticker!"""

    text = animu.pattern_match.group(1)
    if not text:
        if animu.is_reply:
            text = (await animu.get_reply_message()).message
        else:
            await animu.edit("You haven't written any article, Waifu is going away.")
            return
    animus = [1, 3, 7, 9, 13, 22, 34, 35, 36, 37, 43, 44, 45, 52, 53, 55]
    sticcers = await animu.client.inline_query(
        "stickerizerbot", f"#{random.choice(animus)}{(deEmojify(text))}"
    )
    await sticcers[0].click(
        animu.chat_id,
        reply_to=animu.reply_to_msg_id,
        silent=True if animu.is_reply else False,
        hide_via=True,
    )
    await animu.delete()


async def _bash(event):
    if event.fwd_from:
        return
    _tg = await get_pika_tg(event)
    PROCESS_RUN_TIME = 100
    cmd = event.pattern_match.group(1)
    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    time.time() + PROCESS_RUN_TIME
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    e = stderr.decode()
    if not e:
        e = "No Error"
    o = stdout.decode()
    if not o:
        o = "**Tip**: \n`If you want to see the results of your code, I suggest printing them to stdout.`"
    else:
        _o = o.split("\n")
        o = "`\n".join(_o)
    OUTPUT = f"**Qᴜᴇʀʏ:**\n**Cᴏᴍᴍᴀɴᴅ:**\n`{cmd}` \n**Pɪᴅ**\n`{process.pid}`\n\n**Sᴛᴅᴇʀʀ:** \n`{e}`\n**Oᴜᴛᴘᴜᴛ:**\n{o}"
    if len(OUTPUT) > 4095:
        with io.BytesIO(str.encode(OUTPUT)) as out_file:
            out_file.name = "exec.text"
            await event.client.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption=cmd,
                reply_to=reply_to_id,
            )
            await event.delete()
    await pika_msg(event, OUTPUT, _tg)


async def batch_upload(event):
    if event.fwd_from:
        return
    temp_dir = Config.TEMP_DIR
    if os.path.exists(temp_dir):
        files = sorted(os.listdir(temp_dir))
        await event.edit("Uploading Files on Telegram...")
        for file in files:
            required_file_name = temp_dir + "/" + file
            print(required_file_name)
            await event.client.send_file(
                event.chat_id, required_file_name, force_document=True
            )
    else:
        await event.edit("Directory Not Found.")
        return
    await event.edit("Successfull.")


async def belo(event):

    if event.fwd_from:

        return
    _tg = await get_pika_tg(event)
    a = await pika_msg(event, "Typing...", _tg)

    await asyncio.sleep(2)

    x = random.randrange(1, 96)

    if x == 1:

        await pika_msg(
            a, '`"Underwater bubbles and raindrops are total opposites of each other."`'
        )

    if x == 2:

        await pika_msg(
            a, '`"If you buy an eraser you are literally paying for your mistakes."`'
        )

    if x == 3:

        await pika_msg(
            a,
            '`"The Person you care for most has the potential to destroy you the most."`',
        )

    if x == 4:

        await pika_msg(
            a,
            '`"If humans colonize the moon, it will probably attract retirement homes as the weaker gravity will allow the elderly to feel stronger."`',
        )

    if x == 5:

        await pika_msg(
            a, '`"Any video with “wait for it” in the title is simply too long."`'
        )

    if x == 6:

        await pika_msg(
            a,
            '`"Your age in years is how many times you’ve circled the Sun, but your age in months is how many times the Moon has circled you."`',
        )

    if x == 7:

        await pika_msg(
            a,
            '`"Biting your tongue while eating is a perfect example of how you can still screw up, even with decades of experience."`',
        )

    if x == 8:

        await pika_msg(
            a,
            '`"Saying that your home is powered by a wireless Nuclear fusion reactor that is 93 Million miles away sounds way cooler than just saying you have solar panels on your roof."`',
        )

    if x == 9:

        await pika_msg(
            a,
            '`"The most crushing feeling is when someone smiles at you on the street and you don’t react fast enough to smile back."`',
        )

    if x == 10:

        await pika_msg(
            a,
            '`"Teeth constantly require maintenance to prevent their decay when alive, and yet they manage to survive for thousands of years buried as fossils."`',
        )

    if x == 11:

        await pika_msg(a, '`"A folder is for things that you don\'t want to fold."`')

    if x == 12:

        await pika_msg(
            a,
            '`"Waking up in the morning sometimes feels like resuming a shitty movie you decided to quit watching."`',
        )

    if x == 13:

        await pika_msg(
            a, '`"If everything goes seventhly, you probably won\'t remember today."`'
        )

    if x == 14:

        await pika_msg(
            a,
            '`"When you meet new people in real life, you unlock more characters for your dream world."`',
        )

    if x == 15:

        await pika_msg(
            a,
            '`"Maybe if they renamed sunscreen to “anti-cancer cream” more people would wear it."`',
        )

    if x == 16:

        await pika_msg(
            a,
            '`"200 years ago, people would never have guessed that humans in the future would communicate by silently tapping on glass."`',
        )

    if x == 17:

        await pika_msg(
            a,
            '`"Parents worry about what their sons download and worry about what their daughters upload."`',
        )

    if x == 18:

        await pika_msg(
            a,
            '`"It\'s crazy how you can be the same age as someone, but at a completely different stage in your life."`',
        )

    if x == 19:

        await pika_msg(
            a,
            "`\"When you think you wanna die, you really don't wanna die, you just don't wanna live like this.\"`",
        )

    if x == 20:

        await pika_msg(a, '`"Technically, no one has ever been in an empty room."`')

    if x == 21:

        await pika_msg(
            a,
            '`"An onion is the bass player of food. You would probably not enjoy it solo, but you’d miss it if it wasn’t there."`',
        )

    if x == 22:

        await pika_msg(
            a,
            "`\"We run everywhere in videogames because we're too lazy to walk, but In real life we walk everywhere because we're too lazy to run.\"`",
        )

    if x == 23:

        await pika_msg(
            a,
            '`"Every single decision you ever made has brought you to read this sentence."`',
        )

    if x == 24:

        await pika_msg(a, "`\"The word 'quiet' is often said very loud.\"`")

    if x == 25:

        await pika_msg(
            a,
            '`"Everybody wants you to work hard, but nobody wants to hear about how hard you work."`',
        )

    if x == 26:

        await pika_msg(
            a,
            '`"We brush our teeth with hair on a stick and brush our hair with teeth on a stick."`',
        )

    if x == 27:

        await pika_msg(
            a,
            '`"No one remembers your awkward moments but they’re too busy remembering their own."`',
        )

    if x == 28:

        await pika_msg(
            a,
            '`"Dumb people try to say simple ideas as complex as possible while smart people try to say complex ideas as simple as possible."`',
        )

    if x == 29:

        await pika_msg(
            a,
            "`\"Some people think they're better than you because they grew up richer. Some people think they're better than you because they grew up poorer.\"`",
        )

    if x == 30:

        await pika_msg(
            a,
            '`"The biggest irony is that computers & mobiles were invented to save out time!"`',
        )

    if x == 31:

        await pika_msg(
            a,
            '`"After honey was first discovered, there was likely a period where people were taste testing any available slime from insects."`',
        )

    if x == 32:

        await pika_msg(
            a,
            '`"You know you’re getting old when your parents start disappointing you, instead of you disappointing them."`',
        )

    if x == 33:

        await pika_msg(
            a,
            '`"Humans are designed to learn through experience yet the education system has made it so we get no experience."`',
        )

    if x == 34:

        await pika_msg(
            a, '`"By focusing on blinking, you blink slower... Same for breathing."`'
        )

    if x == 35:

        await pika_msg(
            a,
            '`"Drivers in a hurry to beat traffic usually cause the accidents which create the traffic they were trying to avoid."`',
        )

    if x == 36:

        await pika_msg(
            a,
            '`"Characters that get married in fiction were literally made for each other."`',
        )

    if x == 37:

        await pika_msg(
            a,
            '`"Babies are a clean hard drive that can be programmed with any language."`',
        )

    if x == 38:

        await pika_msg(
            a,
            "`\"There could be a miracle drug that cures every disease to man, that we'll never know about because it doesn't work on rats.\"`",
        )

    if x == 39:

        await pika_msg(
            a,
            "`\"Rhinos evolved to grow a horn for protection, but it's what's making them go extinct.\"`",
        )

    if x == 40:

        await pika_msg(
            a,
            '`"Maybe we don\'t find time travelers because we all die in 25-50 years."`',
        )

    if x == 41:

        await pika_msg(
            a,
            '`"Sleep is the trial version of death, It even comes with ads based on your activity."`',
        )

    if x == 42:

        await pika_msg(
            a,
            '`"The most unrealistic thing about Spy movies is how clean the air ventilation system is!"`',
        )

    if x == 43:

        await pika_msg(
            a,
            '`"In games we play through easy modes to unlock hard modes. In life we play through hard modes to unlock easy modes."`',
        )

    if x == 44:

        await pika_msg(
            a,
            '`"Silent people seem smarter than loud people, because they keep their stupid thoughts to themselves."`',
        )

    if x == 45:

        await pika_msg(a, '`"If Greenland actually turns green, we\'re all screwed."`')

    if x == 46:

        await pika_msg(
            a,
            '`"If someone says clever things in your dream, it actually shows your own cleverness."`',
        )

    if x == 47:

        await pika_msg(
            a,
            '`"Famous movie quotes are credited to the actor and not the actual writer who wrote them."`',
        )

    if x == 48:

        await pika_msg(
            a,
            '`"No one actually teaches you how to ride a bicycle. They just hype you up until you work it out."`',
        )

    if x == 49:

        await pika_msg(a, '`"Ask yourself why the the brain ignores the second the."`')

    if x == 50:

        await pika_msg(
            a,
            '`"You’ve probably forgot about 80% of your entire life and most of the memories you do remember are not very accurate to what actually happened."`',
        )

    if x == 51:

        await pika_msg(
            a,
            '`"It will be a lot harder for kids to win against their parents in video games in the future."`',
        )

    if x == 52:

        await pika_msg(
            a,
            '`"Everyone has flaws, if you don\'t recognize yours, you have a new one."`',
        )

    if x == 53:

        await pika_msg(a, '`"Raising a child is training your replacement."`')

    if x == 54:

        await pika_msg(
            a,
            "`\"'O'pen starts with a Closed circle, and 'C'lose starts with an open circle.\"`",
        )

    if x == 55:

        await pika_msg(
            a,
            '`"There\'s always someone who hated you for no reason, and still does."`',
        )

    if x == 56:

        await pika_msg(
            a,
            '`"After popcorn was discovered, there must have been a lot of random seeds that were roasted to see if it would have the same effect."`',
        )

    if x == 57:

        await pika_msg(
            a,
            '`"The more important a good night\'s sleep is, the harder it is to fall asleep."`',
        )

    if x == 58:

        await pika_msg(
            a,
            '`"Blessed are those that can properly describe the type of haircut they want to a new stylist."`',
        )

    if x == 59:

        await pika_msg(
            a,
            "`\"Too many people spend money they haven't earned, to buy things they don't want, to impress people they don't like!\"`",
        )

    if x == 60:

        await pika_msg(
            a,
            '`"Theme park employees must be good at telling the difference between screams of horror and excitement."`',
        )

    if x == 61:

        await pika_msg(a, '`"6 to 6:30 feels more half-an-hour than 5:50 to 6:20"`')

    if x == 62:

        await pika_msg(
            a,
            '`"Getting your password right on the last login attempt before lockout is the closest thing to disarming a bomb at the last minute that most of us will experience."`',
        )

    if x == 63:

        await pika_msg(
            a,
            '`"Listening to podcasts before bed is the adult version of story-time."`',
        )

    if x == 64:

        await pika_msg(
            a,
            '`"If all criminals stopped robbing then the security industry would fall in which they could then easily go back to robbing."`',
        )

    if x == 65:

        await pika_msg(a, '`"A ton of whales is really only like half a whale."`')

    if x == 66:

        await pika_msg(
            a,
            '`"When you get old, the old you is technically the new you, and your young self is the old you."`',
        )

    if x == 67:

        await pika_msg(
            a,
            '`"You probably won\'t find many negative reviews of parachutes on the Internet."`',
        )

    if x == 68:

        await pika_msg(
            a,
            '`"We show the most love and admiration for people when they\'re no longer around to appreciate it."`',
        )

    if x == 69:

        await pika_msg(
            a,
            "`\"We've practiced sleeping thousands of times, yet can't do it very well or be consistent.\"`",
        )

    if x == 70:

        await pika_msg(
            a,
            '`"Humans are more enthusiastic about moving to another planet with hostile environment than preserving earth - the planet they are perfectly shaped for."`',
        )

    if x == 71:

        await pika_msg(
            a,
            "`\"The happiest stage of most people's lives is when their brains aren't fully developed yet.\"`",
        )

    if x == 72:

        await pika_msg(a, '`"The most effective alarm clock is a full bladder."`')

    if x == 73:

        await pika_msg(
            a, '`"You probably just synchronized blinks with millions of people."`'
        )

    if x == 74:

        await pika_msg(
            a,
            '`"Since we test drugs on animals first, rat medicine must be years ahead of human medicine."`',
        )

    if x == 75:

        await pika_msg(
            a, '`"Night before a day off is more satisfying than the actual day off."`'
        )

    if x == 76:

        await pika_msg(a, '`"We put paper in a folder to keep it from folding."`')

    if x == 77:

        await pika_msg(
            a, '`"Somewhere, two best friends are meeting for the first time."`'
        )

    if x == 78:

        await pika_msg(
            a,
            '`"Our brain simultaneously hates us, loves us, doesn\'t care about us, and micromanages our every move."`',
        )

    if x == 79:

        await pika_msg(
            a,
            '`"Being a male is a matter of birth. Being a man is a matter of age. But being a gentleman is a matter of choice."`',
        )

    if x == 80:

        await pika_msg(
            a,
            '`"Soon the parents will be hiding their social account from their kids rather than kids hiding their accounts from the parents."`',
        )

    if x == 81:

        await pika_msg(a, '`"Wikipedia is what the internet was meant to be."`')

    if x == 82:

        await pika_msg(
            a,
            '`"A theme park is the only place that you can hear screams in the distance and not be concerned."`',
        )

    if x == 83:

        await pika_msg(
            a,
            '`"A wireless phone charger offers less freedom of movement than a wired one."`',
        )

    if x == 84:

        await pika_msg(
            a,
            "`\"If you repeatedly criticize someone for liking something you don't, they won't stop liking it. They'll stop liking you.\"`",
        )

    if x == 85:

        await pika_msg(
            a,
            '`"Somewhere there is a grandmother, whose grandson really is the most handsome boy in the world."`',
        )

    if x == 86:

        await pika_msg(
            a,
            '`"If someday human teleportation becomes real, people will still be late for work."`',
        )

    if x == 87:

        await pika_msg(
            a,
            '`"The first humans who ate crabs must have been really hungry to try and eat an armored sea spider"`',
        )

    if x == 88:

        await pika_msg(
            a, '`"Doing something alone is kind of sad, but doing it solo is cool af."`'
        )

    if x == 89:

        await pika_msg(
            a,
            '`"Your brain suddenly becomes perfect at proofreading after you post something."`',
        )

    if x == 90:

        await pika_msg(
            a,
            '`"There\'s always that one song in your playlist that you always skip but never remove."`',
        )

    if x == 91:

        await pika_msg(
            a,
            '`"Kids next century will probably hate us for taking all the good usernames."`',
        )

    if x == 92:

        await pika_msg(a, '`"Bubbles are to fish what rain is to humans."`')

    if x == 93:

        await pika_msg(
            a,
            '`"The more people you meet, the more you realise and appreciate how well your parents raised you."`',
        )

    if x == 94:

        await pika_msg(a, '`"A comma is a short pause, a coma is a long pause."`')

    if x == 95:

        await pika_msg(a, '`"Someday you will either not wake up or not go to sleep."`')

    if x == 96:

        await pika_msg(
            a, '`"Bermuda Triangle might be the exit portal of this simulation."`'
        )

    if x == 97:

        await pika_msg(
            a,
            '`"If we put solar panels above parking lots, then our cars wouldn\'t get hot and we would have a lot of clean energy."`',
        )


async def bombs(event):
    if event.fwd_from:
        return
    _tg = await get_pika_tg(event)
    a = await pika_msg(
        event, "▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n", _tg
    )
    await asyncio.sleep(0.5)
    await pika_msg(a, "💣💣💣💣 \n▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n")
    await asyncio.sleep(0.5)
    await pika_msg(a, "▪️▪️▪️▪️ \n💣💣💣💣 \n▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n")
    await asyncio.sleep(0.5)
    await pika_msg(a, "▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n💣💣💣💣 \n▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n")
    await asyncio.sleep(0.5)
    await pika_msg(a, "▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n💣💣💣💣 \n▪️▪️▪️▪️ \n")
    await asyncio.sleep(0.5)
    await pika_msg(a, "▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n💣💣💣💣 \n")
    await asyncio.sleep(1)
    await pika_msg(a, "▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n💥💥💥💥 \n")
    await asyncio.sleep(0.5)
    await pika_msg(a, "▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n💥💥💥💥 \n💥💥💥💥 \n")
    await asyncio.sleep(0.5)
    await pika_msg(a, "▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n😵😵😵😵 \n")
    await asyncio.sleep(0.5)
    await pika_msg(a, "`RIP PLOXXX......`")
    await asyncio.sleep(2)


async def call(event):
    if event.fwd_from:
        return
    _tg = await get_pika_tg(event)
    an = await pikaa(event, "ALIVE_NAME")
    animation_interval = 3
    animation_ttl = range(0, 18)
    await pika_msg(event, "Calling", _tg)
    animation_chars = [
        "`Connecting To Telegram Headquarters...`",
        "`Call Connected.`",
        "`Telegram: Hello This is Telegram HQ. Who is this?`",
        f"`Me: Yo this is **{an}**,`Please Connect me to my idiot bro,Ayush Durov`",
        "`User Authorised.`",
        "`Calling Pavel Durov`  `At +916969696969`",
        "`Private  Call Connected...`",
        "`Me: Hello Sir, Please Ban This Telegram Account.`",
        "`Pavel: May I Know Who Is This?`",
        f"`Me: Yo Brah, I Am`**{an}**",
        "`Pavel: OMG!!! Long time no see, Wassup Brother...\nI'll Make Sure That Guy Account Will Get Blocked Within 24Hrs.`",
        "`Me: Thanks, See You Later Brah.`",
        "`Pavel: Please Don't Thank Brah, Telegram Is Our's. Just Gimme A Call When You Become Free.`",
        "`Me: Is There Any Issue/Emergency???`",
        "`Pavel: Yes Sur, There Is A Bug In Telegram v69.6.9.\nI Am Not Able To Fix It. If Possible, Please Help Fix The Bug.`",
        "`Me: Send Me The App On My Telegram Account, I Will Fix The Bug & Send You.`",
        "`Pavel: Sure Sur \nTC Bye Bye :)`",
        "`Private Call Disconnected.`",
    ]

    for i in animation_ttl:

        await asyncio.sleep(animation_interval)
        await pika_msg(a, animation_chars[i % 18])


async def spm_notify(event):
    if event.fwd_from:
        return
    mentions = "@admin: **Spam Spotted**"
    chat = await event.get_input_chat()
    async for x in event.client.iter_participants(
        chat, filter=ChannelParticipantsAdmins
    ):
        mentions += f"[\u2063](tg://user?id={x.id})"
    reply_message = None
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        await reply_message.reply(mentions)
    else:
        await event.reply(mentions)
    await event.delete()


async def _carbon(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@"):
        """ A Wrapper for carbon.now.sh """
        _tg = await get_pika_tg(e)
        a = await pika_msg(e, "`Processing..`", _tg)
        CARBON = "https://carbon.now.sh/?l={lang}&code={code}"
        global CARBONLANG
        textx = await e.get_reply_message()
        pcode = e.text
        if pcode[8:]:
            pcode = str(pcode[8:])
        elif textx:
            pcode = str(textx.message)

        code = quote_plus(pcode)
        await pika_msg(a, "`Meking Carbon...\n25%`")
        url = CARBON.format(code=code, lang=CARBONLANG)
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.binary_location = GOOGLE_CHROME_BIN
        chrome_options.add_argument("--window-size=1920x1080")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-gpu")
        prefs = {"download.default_directory": "./"}
        chrome_options.add_experimental_option("prefs", prefs)
        driver = webdriver.Chrome(
            executable_path=CHROME_DRIVER,
            options=chrome_options)
        driver.get(url)
        await pika_msg(a, "`Be Patient...\n50%`")
        download_path = "./"
        driver.command_executor._commands["send_command"] = (
            "POST",
            "/session/$sessionId/chromium/send_command",
        )
        params = {
            "cmd": "Page.setDownloadBehavior",
            "params": {"behavior": "allow", "downloadPath": download_path},
        }
        driver.execute("send_command", params)
        driver.find_element_by_xpath(
            "//button[contains(text(),'Export')]").click()
        await pika_msg(a, "`Processing..\n75%`")
        sleep(1)
        await pika_msg(a, "`Done Dana Done...\n100%`")
        file = "./carbon.png"
        await pika_msg(a, "`Uploading..`")
        await e.client.send_file(
            e.chat_id,
            file,
            caption="<< Here's your carbon, \n Carbonised by [PikaBot](t.me/PikachuUserBot)>> ",
            force_document=True,
            reply_to=e.message.reply_to_msg_id,
        )
        os.remove("./carbon.png")
        driver.quit()
        await e.delete()  # Deleting msg


async def _chain(event):
    await event.edit("Counting...")
    count = -1
    message = event.message
    while message:
        reply = await message.get_reply_message()
        if reply is None:
            await event.client(
                SaveDraftRequest(
                    await event.get_input_chat(), "", reply_to_msg_id=message.id
                )
            )
        message = reply
        count += 1
    await event.edit(f"Chain length: {count}")


async def get_media(event):
    if event.fwd_from:
        return
    dir = "./temp/"
    try:
        os.makedirs("./temp/")
    except BaseException:
        pass
    channel_username = event.text
    limit = channel_username[6:9]
    print(limit)
    channel_username = channel_username[11:]
    print(channel_username)
    await event.edit("Downloading Media From this Channel.")
    msgs = await event.client.get_messages(channel_username, limit=int(limit))
    with open("log.txt", "w") as f:
        f.write(str(msgs))
    for msg in msgs:
        if msg.media is not None:
            await event.client.download_media(msg, dir)
    ps = subprocess.Popen(("ls", "temp"), stdout=subprocess.PIPE)
    output = subprocess.check_output(("wc", "-l"), stdin=ps.stdout)
    ps.wait()
    output = str(output)
    output = output.replace("b'", "")
    output = output.replace("\n'", "")
    await event.edit("Downloaded " + output + " files.")


async def getmedia(event):
    if event.fwd_from:
        return
    dir = "./temp/"
    try:
        os.makedirs("./temp/")
    except BaseException:
        pass
    channel_username = event.text
    channel_username = channel_username[7:]

    print(channel_username)
    await event.edit("Downloading All Media From this Channel.")
    msgs = await event.client.get_messages(channel_username, limit=3000)
    with open("log.txt", "w") as f:
        f.write(str(msgs))
    for msg in msgs:
        if msg.media is not None:
            await event.client.download_media(msg, dir)
    ps = subprocess.Popen(("ls", "temp"), stdout=subprocess.PIPE)
    output = subprocess.check_output(("wc", "-l"), stdin=ps.stdout)
    ps.wait()
    output = str(output)
    output = output.replace("b'", "")
    output = output.replace("\n'", "")
    await event.edit("Downloaded " + output + " files.")


async def _ctg(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await event.edit("```Reply to a Link.```")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.text:
        await event.edit("```Reply to a Link```")
        return
    chat = "@chotamreaderbot"
    reply_message.sender
    await event.edit("```Processing```")
    async with event.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=272572121)
            )
            await event.client.forward_messages(chat, reply_message)
            response = await response
        except YouBlockedUserError:
            await event.reply("`RIP Check Your Blacklist Boss`")
            return
        if response.text.startswith(""):
            await event.edit("Am I Dumb Or Am I Dumb?")
        else:
            await event.delete()
            await event.client.send_message(event.chat_id, response.message)


async def cflip(event):
    if event.fwd_from:
        return
    r = random.randint(1, 100)
    input_str = event.pattern_match.group(1)
    if input_str:
        input_str = input_str.lower()
    if r % 2 == 1:
        if input_str == "heads":
            await event.edit("The coin landed on: **Heads**. \n You were correct.")
        elif input_str == "tails":
            await event.edit(
                "The coin landed on: **Heads**. \n You weren't correct, try again ..."
            )
        else:
            await event.edit("The coin landed on: **Heads**.")
    elif r % 2 == 0:
        if input_str == "tails":
            await event.edit("The coin landed on: **Tails**. \n You were correct.")
        elif input_str == "heads":
            await event.edit(
                "The coin landed on: **Tails**. \n You weren't correct, try again ..."
            )
        else:
            await event.edit("The coin landed on: **Tails**.")
    else:
        await event.edit(r"¯\_(ツ)_/¯")


async def findcolour(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    message_id = event.message.id
    if event.reply_to_msg_id:
        message_id = event.reply_to_msg_id
    if input_str.startswith("#"):
        try:
            usercolor = ImageColor.getrgb(input_str)
        except Exception as e:
            await event.edit(str(e))
            return False
        else:
            im = Image.new(mode="RGB", size=(1280, 720), color=usercolor)
            im.save("UniBorg.png", "PNG")
            input_str = input_str.replace("#", "#COLOR_")
            await event.client.send_file(
                event.chat_id,
                "PikaBot.png",
                force_document=False,
                caption=input_str,
                reply_to=message_id,
            )
            os.remove("PikaBot.png")
            await event.delete()
    else:
        await event.edit("Syntax: `.color <color_code>`")


async def _congo(event):
    if event.fwd_from:
        return
    bro = random.randint(0, len(CongoStr) - 1)
    reply_text = CongoStr[bro]
    await event.edit(reply_text)


async def _convoqt(event):
    if event.fwd_from:
        return
    await event.edit("selecting question...")
    await asyncio.sleep(2)
    x = random.randrange(1, 60)

    if x == 1:
        await event.edit(
            '`"Arrange them in descending order of importance – MONEY, LOVE, FAMILY, CAREER, FRIENDS."`'
        )

    if x == 2:

        await event.edit(
            '`"If you had to change your name, what would your new name be, and why would you choose that name?"`'
        )

    if x == 3:

        await event.edit(
            '`"What’s the most interesting thing you’ve read or seen this week?"`'
        )

    if x == 4:

        await event.edit('`"What scene from a TV show will you never forget?"`')

    if x == 5:

        await event.edit(
            '`"If you could become a master in one skill, what skill would you choose?"`'
        )

    if x == 6:

        await event.edit('`"What three words can describe you?"`')

    if x == 7:

        await event.edit(
            '`"If you had to delete one app from your phone, what would it be?"`'
        )

    if x == 8:

        await event.edit(
            '`"Would you go out with me if I was the last person on earth?"`'
        )

    if x == 9:

        await event.edit('`"If you switched genders for the day, what would you do?"`')

    if x == 10:

        await event.edit(
            '`"If you could eat lunch with someone here. Who would you choose?"`'
        )

    if x == 11:

        await event.edit(
            '`"If you were told you only had one week left to live, what would you do?"`'
        )

    if x == 12:

        await event.edit(
            '`"What\'s number one item you would save from your burning house?"`'
        )

    if x == 13:

        await event.edit(
            '`"If you could only text one person for the rest of your life, but you could never talk to that person face to face, who would that be?"`'
        )

    if x == 14:

        await event.edit('`"How many kids do you want to have in the future?"`')

    if x == 15:

        await event.edit(
            '`"Who in this group would be the worst person to date? Why?"`'
        )

    if x == 16:

        await event.edit('`"What does your dream boy or girl look like?"`')

    if x == 17:

        await event.edit(
            '`"What would be in your web history that you’d be embarrassed if someone saw?"`'
        )

    if x == 18:

        await event.edit('`"Do you sing in the shower?"`')

    if x == 19:

        await event.edit('`"What’s the right age to get married?"`')

    if x == 20:

        await event.edit('`"What are your top 5 rules for life?"`')

    if x == 21:

        await event.edit(
            '`"If given an option, would you choose a holiday at the beach or in the mountains?"`'
        )

    if x == 22:

        await event.edit(
            '`"If you are made the president of your country, what would be the first thing that you will do?"`'
        )

    if x == 23:

        await event.edit(
            '`"If given a chance to meet 3 most famous people on the earth, who would it be, answer in order of preference."`'
        )

    if x == 24:

        await event.edit(
            '`"Have you ever wished to have a superpower, if so, what superpower you would like to have?"`'
        )

    if x == 25:

        await event.edit(
            '`"Can you spend an entire day without phone and internet? If yes, what would you do?"`'
        )

    if x == 26:

        await event.edit('`"Live-in relation or marriage, what do you prefer?"`')

    if x == 27:

        await event.edit('`"What is your favorite cuisine or type of food?"`')

    if x == 28:

        await event.edit(
            '`"What are some good and bad things about the education system in your country?"`'
        )

    if x == 29:

        await event.edit('`"What do you think of online education?"`')

    if x == 30:

        await event.edit('`"What are some goals you have failed to accomplish?"`')

    if x == 31:

        await event.edit('`"Will technology save the human race or destroy it?"`')

    if x == 32:

        await event.edit('`"What was the best invention of the last 50 years?"`')

    if x == 33:

        await event.edit(
            '`"Have you travelled to any different countries? Which ones?"`'
        )

    if x == 34:

        await event.edit(
            '`"Which sport is the most exciting to watch? Which is the most boring to watch?"`'
        )

    if x == 35:

        await event.edit('`"What’s the most addictive mobile game you have played?"`')

    if x == 36:

        await event.edit('`"How many apps do you have on your phone?"`')

    if x == 37:

        await event.edit('`"What was the last song you listened to?"`')

    if x == 38:

        await event.edit(
            '`"Do you prefer to watch movies in the theater or in the comfort of your own home?"`'
        )

    if x == 39:

        await event.edit('`"Do you like horror movies? Why or why not?"`')

    if x == 40:

        await event.edit(
            '`"How often do you help others? Who do you help? How do you help?"`'
        )

    if x == 41:

        await event.edit('`"What song do you play most often?"`')

    if x == 42:

        await event.edit('`"Suggest a new rule that should be added in this group!"`')

    if x == 43:

        await event.edit('`"What app on your phone do you think I should get?"`')

    if x == 44:

        await event.edit(
            '`"What website or app has completely changed your life for better or for worse?"`'
        )

    if x == 45:

        await event.edit('`"What isn’t real but you desperately wish it was?"`')

    if x == 46:

        await event.edit('`"What thing do you really wish you could buy right now?"`')

    if x == 47:

        await event.edit(
            '`"If you could ban an admin from this group. Who would you prefer ?"`'
        )

    if x == 48:

        await event.edit(
            '`"What would you do if someone left a duffle bag filled with $2,000,000 on your back porch?"`'
        )

    if x == 49:

        await event.edit('`"Who is the luckiest person you know?"`')

    if x == 50:

        await event.edit(
            '`"If you could visit someone\'s house in this group, who would it be ?"`'
        )

    if x == 51:

        await event.edit('`"What are you tired of hearing about?"`')

    if x == 52:

        await event.edit(
            '`"If you died today, what would your greatest achievement be?"`'
        )

    if x == 53:

        await event.edit('`"What method will you choose to kill yourself?"`')

    if x == 54:

        await event.edit('`"What’s the best news you\'ve heard in the last 24 hours?"`')

    if x == 55:

        await event.edit(
            '`"What is the most important change that should be made to your country’s education system?"`'
        )

    if x == 56:

        await event.edit('`"Send your favourite sticker pack."`')

    if x == 57:

        await event.edit('`"Send your favourite animated sticker pack."`')

    if x == 58:

        await event.edit('`"Send your favourite video or gif."`')

    if x == 59:

        await event.edit('`"Send your favourite emojies"`')

    if x == 60:

        await event.edit(
            '`"What’s something you misunderstood as a child and only realized much later was wrong?"`'
        )


async def decide(event):
    if event.fwd_from:
        return
    message_id = event.message.id
    if event.reply_to_msg_id:
        message_id = event.reply_to_msg_id
    r = requests.get("https://yesno.wtf/api").json()
    await event.client.send_message(
        event.chat_id, r["answer"], reply_to=message_id, file=r["image"]
    )
    await event.delete()


async def _cry(event):
    if event.fwd_from:
        return
    animation_interval = 1
    animation_ttl = range(0, 103)
    await event.edit("crying")
    animation_chars = [
        ";__",
        ";___",
        ";____",
        ";_____",
        ";______",
        ";_______",
        ";________",
        ";__________",
        ";____________",
        ";______________",
        ";________________",
        ";__________________",
        ";____________________",
        ";______________________",
        ";________________________",
        ";_________________________",
        ";_________________________",
        ";________________________",
        ";_______________________",
        ";______________________",
        ";_____________________",
        ";____________________",
        ";___________________",
        ";__________________",
        ";_________________",
        ";________________",
        ";_______________",
        ";_____________",
        ";___________",
        ";_________",
        ";_______",
        ";_____",
        ";____",
        ";___",
        ";__",
        ";You made me `CRY`",
    ]

    for i in animation_ttl:

        await asyncio.sleep(animation_interval)
        await event.edit(animation_chars[i % 35])


async def deepfryer(event):
    try:
        frycount = int(event.pattern_match.group(1))
        if frycount < 1:
            raise ValueError
    except ValueError:
        frycount = 1

    if event.is_reply:
        reply_message = await event.get_reply_message()
        data = await check_media(reply_message)

        if isinstance(data, bool):
            await event.edit("`I can't deep fry that!`")
            return
    else:
        await event.edit("`Reply to an image or sticker to deep fry it!`")
        return

    # download last photo (highres) as byte array
    await event.edit("`Downloading media…`")
    image = io.BytesIO()
    await event.client.download_media(data, image)
    image = Image.open(image)

    # fry the image
    await event.edit("`Deep frying media…`")
    for _ in range(frycount):
        image = await deepfry(image)

    fried_io = io.BytesIO()
    fried_io.name = "image.jpeg"
    image.save(fried_io, "JPEG")
    fried_io.seek(0)

    await event.reply(file=fried_io)


async def deepfry(img: Image) -> Image:
    colours = (
        (randint(50, 200), randint(40, 170), randint(40, 190)),
        (randint(190, 255), randint(170, 240), randint(180, 250)),
    )

    img = img.copy().convert("RGB")

    # Crush image to hell and back
    img = img.convert("RGB")
    width, height = img.width, img.height
    img = img.resize(
        (int(width ** uniform(0.8, 0.9)), int(height ** uniform(0.8, 0.9))),
        resample=Image.LANCZOS,
    )
    img = img.resize(
        (int(width ** uniform(0.85, 0.95)), int(height ** uniform(0.85, 0.95))),
        resample=Image.BILINEAR,
    )
    img = img.resize(
        (int(width ** uniform(0.89, 0.98)), int(height ** uniform(0.89, 0.98))),
        resample=Image.BICUBIC,
    )
    img = img.resize((width, height), resample=Image.BICUBIC)
    img = ImageOps.posterize(img, randint(3, 7))

    # Generate colour overlay
    overlay = img.split()[0]
    overlay = ImageEnhance.Contrast(overlay).enhance(uniform(1.0, 2.0))
    overlay = ImageEnhance.Brightness(overlay).enhance(uniform(1.0, 2.0))

    overlay = ImageOps.colorize(overlay, colours[0], colours[1])

    # Overlay red and yellow onto main image and sharpen the hell out of it
    img = Image.blend(img, overlay, uniform(0.1, 0.4))
    img = ImageEnhance.Sharpness(img).enhance(randint(5, 300))

    return img


async def check_media(reply_message):
    if reply_message and reply_message.media:
        if reply_message.photo:
            data = reply_message.photo
        elif reply_message.document:
            if (
                DocumentAttributeFilename(file_name="AnimatedSticker.tgs")
                in reply_message.media.document.attributes
            ):
                return False
            if (
                reply_message.gif
                or reply_message.video
                or reply_message.audio
                or reply_message.voice
            ):
                return False
            data = reply_message.media.document
        else:
            return False
    else:
        return False

    if not data or data is None:
        return False
    else:
        return data


async def remppic(delpfp):
    """ For .delpfp command, delete your current profile picture in Telegram. """
    group = delpfp.text[8:]
    if group == "all":
        lim = 0
    elif group.isdigit():
        lim = int(group)
    else:
        lim = 1

    pfplist = await delpfp.client(
        GetUserPhotosRequest(user_id=delpfp.sender_id, offset=0, max_id=0, limit=lim)
    )
    input_photos = []
    for sep in pfplist.photos:
        input_photos.append(
            InputPhoto(
                id=sep.id,
                access_hash=sep.access_hash,
                file_reference=sep.file_reference,
            )
        )
    await delpfp.client(DeletePhotosRequest(id=input_photos))
    await delpfp.edit(f"`Successfully deleted {len(input_photos)} profile picture(s).`")


async def jon(event):
    if event.fwd_from:
        return
    mentions = "`━━━━━┓ \n┓┓┓┓┓┃\n┓┓┓┓┓┃　ヽ○ノ ⇦ Me When You Joined \n┓┓┓┓┓┃.     /　 \n┓┓┓┓┓┃ ノ) \n┓┓┓┓┓┃\n┓┓┓┓┓┃\n┓┓┓┓┓┃\n┓┓┓┓┓┃\n┓┓┓┓┓┃\n┓┓┓┓┓┃\n┓┓┓┓┓┃\n┓┓┓┓┓┃\n┓┓┓┓┓┃\n┓┓┓┓┓┃\n┓┓┓┓┓┃\n┓┓┓┓┓┃\n┓┓┓┓┓┃\n┓┓┓┓┓┃\n┓┓┓┓┓┃\n┓┓┓┓┓┃`"
    chat = await event.get_input_chat()
    async for x in event.client.iter_participants(
        chat, filter=ChannelParticipantsAdmins
    ):
        mentions += f""
    reply_message = None
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        await reply_message.reply(mentions)
    else:
        await event.reply(mentions)
    await event.delete()


async def pay(event):
    if event.fwd_from:
        return
    mentions = "`█▀▀▀▀▀█░▀▀░░░█░░░░█▀▀▀▀▀█\n█░███░█░█▄░█▀▀░▄▄░█░███░█\n█░▀▀▀░█░▀█▀▀▄▀█▀▀░█░▀▀▀░█\n▀▀▀▀▀▀▀░▀▄▀▄▀▄█▄▀░▀▀▀▀▀▀▀\n█▀█▀▄▄▀░█▄░░░▀▀░▄█░▄▀█▀░▀\n░█▄▀░▄▀▀░░░▄▄▄█░▀▄▄▄▀▄▄▀▄\n░░▀█░▀▀▀▀▀▄█░▄░████ ██▀█▄\n▄▀█░░▄▀█▀█▀░█▄▀░▀█▄██▀░█▄\n░░▀▀▀░▀░█▄▀▀▄▄░▄█▀▀▀█░█▀▀\n█▀▀▀▀▀█░░██▀█░░▄█░▀░█▄░██\n█░███░█░▄▀█▀██▄▄▀▀█▀█▄░▄▄\n█░▀▀▀░█░█░░▀▀▀░█░▀▀▀▀▄█▀░\n▀▀▀▀▀▀▀░▀▀░░▀░▀░░░▀▀░▀▀▀▀`"
    chat = await event.get_input_chat()
    async for x in event.client.iter_participants(
        chat, filter=ChannelParticipantsAdmins
    ):
        mentions += f""
    reply_message = None
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        await reply_message.reply(mentions)
    else:
        await event.reply(mentions)
    await event.delete()


async def dict(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    input_url = "https://bots.shrimadhavuk.me/dictionary/?s={}".format(
        input_str)
    headers = {"USER-AGENT": "PikaBot"}
    caption_str = f"Meaning of __{input_str}__\n"
    try:
        response = requests.get(input_url, headers=headers).json()
        pronounciation = response.get("p")
        meaning_dict = response.get("lwo")
        for current_meaning in meaning_dict:
            current_meaning_type = current_meaning.get("type")
            current_meaning_definition = current_meaning.get("definition")
            caption_str += (
                f"**{current_meaning_type}**: {current_meaning_definition}\n\n"
            )
    except Exception as e:
        caption_str = str(e)
    reply_msg_id = event.message.id
    if event.reply_to_msg_id:
        reply_msg_id = event.reply_to_msg_id
    try:
        await event.client.send_file(
            event.chat_id,
            pronounciation,
            caption=f"Pronounciation of __{input_str}__",
            force_document=False,
            reply_to=reply_msg_id,
            allow_cache=True,
            voice_note=True,
            silent=True,
            supports_streaming=True,
        )
    except BaseException:
        pass
    await event.edit(caption_str)


async def _ding(event):
    if event.fwd_from:
        return
    animation_interval = 0.5
    animation_ttl = range(0, 10)
    await event.edit("dong")
    animation_chars = [
        "🔴⬛⬛⬜⬜\n⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜",
        "⬜⬜⬛⬜⬜\n⬜⬛⬜⬜⬜\n🔴⬜⬜⬜⬜",
        "⬜⬜⬛⬜⬜\n⬜⬜⬛⬜⬜\n⬜⬜🔴⬜⬜",
        "⬜⬜⬛⬜⬜\n⬜⬜⬜⬛⬜\n⬜⬜⬜⬜🔴",
        "⬜⬜⬛⬛🔴\n⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜",
        "⬜⬜⬛⬜⬜\n⬜⬜⬜⬛⬜\n⬜⬜⬜⬜🔴",
        "⬜⬜⬛⬜⬜\n⬜⬜⬛⬜⬜\n⬜⬜🔴⬜⬜",
        "⬜⬜⬛⬜⬜\n⬜⬛⬜⬜⬜\n🔴⬜⬜⬜⬜",
        "🔴⬛⬛⬜⬜\n⬜⬜⬜⬜⬜\n⬜⬜⬜⬜⬜",
        "⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜\n⬜[I Am Here mdafuk'in Bitch](t.me/PikachuUserbot) ⬜\n⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜",
    ]

    for i in animation_ttl:

        await asyncio.sleep(animation_interval)

        await event.edit(animation_chars[i % 10])


async def dlg(request):
    """ direct links generator """
    await request.edit("`Processing...`")
    textx = await request.get_reply_message()
    message = request.pattern_match.group(1)
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        await request.edit("`Usage: .direct <url>`")
        return
    reply = ""
    links = re.findall(r"\bhttps?://.*\.\S+", message)
    if not links:
        reply = "`No links found!`"
        await request.edit(reply)
    for link in links:
        if "drive.google.com" in link:
            reply += gdrive(link)
        elif "zippyshare.com" in link:
            reply += zippy_share(link)
        elif "yadi.sk" in link:
            reply += yandex_disk(link)
        elif "cloud.mail.ru" in link:
            reply += cm_ru(link)
        elif "mediafire.com" in link:
            reply += mediafire(link)
        elif "sourceforge.net" in link:
            reply += sourceforge(link)
        elif "osdn.net" in link:
            reply += osdn(link)
        elif "androidfilehost.com" in link:
            reply += androidfilehost(link)
        else:
            reply += re.findall(r"\bhttps?://(.*?[^/]+)",
                                link)[0] + "is not supported"
    await request.edit(reply)


async def _dns(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    sample_url = "https://da.gd/dns/{}".format(input_str)
    response_api = requests.get(sample_url).text
    if response_api:
        await event.edit("DNS records of {} are \n{}".format(input_str, response_api))
    else:
        await event.edit("i can't seem to find {} on the internet".format(input_str))


async def urlx(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    sample_url = "https://da.gd/s?url={}".format(input_str)
    response_api = requests.get(sample_url).text
    if response_api:
        await event.edit("Generated {} for {}.".format(response_api, input_str))
    else:
        await event.edit("something is wrong. please try again later.")


async def unshort(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    if not input_str.startswith("http"):
        input_str = "http://" + input_str
    r = requests.get(input_str, allow_redirects=False)
    if str(r.status_code).startswith("3"):
        await event.edit(
            "Input URL: {}\nReDirected URL: {}".format(input_str, r.headers["Location"])
        )
    else:
        await event.edit(
            "Input URL {} returned status_code {}".format(input_str, r.status_code)
        )


async def ducgo(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    sample_url = "https://duckduckgo.com/?q={}".format(
        input_str.replace(" ", "+"))
    if sample_url:
        link = sample_url.rstrip()
        await event.edit(
            "Let me 🦆 DuckDuckGo that for you:\n🔎 [{}]({})".format(input_str, link)
        )
    else:
        await event.edit("something is wrong. please try again later.")


async def dump(message):
    try:
        obj = message.pattern_match.group(1)
        if len(obj) != 3:
            raise IndexError
        inp = " ".join(obj)
    except IndexError:
        inp = "🥞 🎂 🍫"
    u, t, g, o, s, n = inp.split(), "🗑", "<(^_^ <)", "(> ^_^)>", "⠀ ", "\n"
    h = [(u[0], u[1], u[2]), (u[0], u[1], ""), (u[0], "", "")]
    for something in reversed(
        [
            y
            for y in (
                [
                    "".join(x)
                    for x in (
                        f + (s, g, s + s * f.count(""), t),
                        f + (g, s * 2 + s * f.count(""), t),
                        f[:i] + (o, f[i], s * 2 + s * f.count(""), t),
                        f[:i] + (s + s * f.count(""), o, f[i], s, t),
                        f[:i] + (s * 2 + s * f.count(""), o, f[i], t),
                        f[:i] + (s * 3 + s * f.count(""), o, t),
                        f[:i] + (s * 3 + s * f.count(""), g, t),
                    )
                ]
                for i, f in enumerate(reversed(h))
            )
        ]
    ):
        for something_else in something:
            await asyncio.sleep(0.3)
            try:
                await message.edit(something_else)
            except errors.MessageIdInvalidError:
                return


async def _eval(event):
    _tg = await get_pika_tg(event)
    if event.fwd_from:
        return
    ax_ = await pika_msg(event, "Processing ...", _tg)
    cmd = event.text.split(" ", maxsplit=1)[1]
    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id

    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None

    try:
        await aexec(cmd, event)
    except Exception:
        exc = traceback.format_exc()

    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr

    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Success"

    final_output = "**EVAL**: `{}` \n\n **OUTPUT**: \n`{}` \n".format(
        cmd, evaluation)

    if len(final_output) > Config.MAX_MESSAGE_SIZE_LIMIT:
        with io.BytesIO(str.encode(final_output)) as out_file:
            out_file.name = "eval.text"
            await event.client.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption=cmd,
                reply_to=reply_to_id,
            )
            await event.delete()
    else:
        await pika_msg(ax_, final_output)


async def aexec(code, event):
    exec(f"async def __aexec(event): " +
         "".join(f"\n {l}" for l in code.split("\n")))
    return await locals()["__aexec"](event)


async def helper(event):
    if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@"):
        tgbotusername = Var.TG_BOT_USER_NAME_BF_HER
        event.pattern_match.group(1)
        if tgbotusername:
            help_string = f"""Pïkå¢hµ Úsêrßð† {helpstr}"""
            results = await event.client.inline_query(  # pylint:disable=E0602
                tgbotusername, help_string
            )
            await results[0].click(
                event.chat_id, reply_to=event.reply_to_msg_id, hide_via=True
            )
            await event.delete()
        else:
            await event.edit("**ERROR:** Set Var TG_BOT_USER_NAME_BF_HER")


if Var.TG_BOT_USER_NAME_BF_HER is not None and tgbot is not None:

    @tgbot.on(events.InlineQuery)  # pylint:disable=E0602
    async def inline_handler(pika_):
        builder = pika_.builder
        result = None
        query = pika_.text
        _pikaa_ = (pika_.query).user_id
        if (
            _pikaa_ == pika_id1
            or _pikaa_ == pika_id2
            or _pikaa_ == pika_id3
            or _pikaa_ == pika_id4
            and query.startswith("Pïkå¢hµ")
        ):
            rev_text = query[::-1]
            buttons = paginate_help(0, bot.pika_cmd, "helpme")
            result = builder.article(
                "©Pikachu Userbot Help",
                text="{}\nCurrently Loaded Plugins: {}".format(
                    query, len(bot.pika_cmd)
                ),
                buttons=buttons,
                link_preview=False,
            )
        await pika_.answer([result] if result else None)

    @tgbot.on(Pika_CallBack(data=re.compile(rb"helpme_next\((.+?)\)")))
    async def _pikacallback(pika_):
        _pikaa_ = (pika_.query).user_id
        if (
            _pikaa_ == pika_id1
            or _pikaa_ == pika_id2
            or _pikaa_ == pika_id3
            or _pikaa_ == pika_id4
        ):
            pikacmds = bot.pika_cmd
            c_p_n = int(pika_.data_match.group(1).decode("UTF-8"))
            buttons = paginate_help(c_p_n + 1, pikacmds, "helpme")
            # https://t.me/TelethonChat/115200
            await pika_.edit(buttons=buttons)

        else:
            _alert_ = "Please get your own PikaBot, and don't use mine!"
            await pika_.answer(_alert_, cache_time=0, alert=True)

    @tgbot.on(Pika_CallBack(data=re.compile(rb"helpme_prev\((.+?)\)")))
    async def _pikacallback(pika_):
        _pikaa_ = (pika_.query).user_id
        if (
            _pikaa_ == pika_id1
            or _pikaa_ == pika_id2
            or _pikaa_ == pika_id3
            or _pikaa_ == pika_id4
        ):
            pikacmds = bot.pika_cmd
            c_p_n = int(pika_.data_match.group(1).decode("UTF-8"))
            buttons = paginate_help(
                c_p_n - 1, pikacmds, "helpme"  # pylint:disable=E0602
            )
            await pika_.edit(buttons=buttons)

        else:
            _alert_ = "Please get your own PikaBot, and don't use mine!"
            await pika_.answer(_alert_, cache_time=0, alert=True)

    @tgbot.on(Pika_CallBack(data=re.compile(b"restart")))
    async def _pikacallback(pika_):
        _pikaa_ = (pika_.query).user_id
        if (
            _pikaa_ == pika_id1
            or _pikaa_ == pika_id2
            or _pikaa_ == pika_id3
            or _pikaa_ == pika_id4
        ):
            await pika_.edit("Pika Pi! Restarting wait for 1 Min!")
            await asyncio.sleep(4)
            await pika_.delete()
            pika_start()
        else:
            _alert_ = "You can't Restart me, Get your own Pikachu Userbot"
            await pika_.answer(_alert_, cache_time=0, alert=True)

    @tgbot.on(Pika_CallBack(data=re.compile(b"close")))
    async def _pikacallback(pika_):
        _pikaa_ = (pika_.query).user_id
        if (
            _pikaa_ == pika_id1
            or _pikaa_ == pika_id2
            or _pikaa_ == pika_id3
            or _pikaa_ == pika_id4
        ):
            _a_ = await pika_.edit("Pika Pi! Menu Closed!")
            await asyncio.sleep(3)
            await _a_.delete()
        else:
            _alert_ = "You can't close this menu ploxx, Get your own Pikachu Userbot"
            await pika_.answer(_alert_, cache_time=0, alert=True)

    @tgbot.on(Pika_CallBack(data=re.compile(b"us_plugin_(.*)")))
    async def _pikacallback(pika_):
        _pikaa_ = (pika_.query).user_id
        if (
            _pikaa_ == pika_id1
            or _pikaa_ == pika_id2
            or _pikaa_ == pika_id3
            or _pikaa_ == pika_id4
        ):

            a = randint(0, 9)
            _rx_ = f"{_emo_[a]}" + f" {rx}"
            _pikacmds = bot.pika_cmd
            _pika_ = pika_.data_match.group(1).decode("UTF-8")
            _pika = _pikacmds[_pika_].__doc__.format(i=_rx_)
            _pikaB = [(custom.Button.inline("⫷BacK", data="pikab"))]
            await pika_.edit(_pika, buttons=_pikaB)

        else:
            ax = os.environ.get("ALIVE_NAME")
            iq = await pika_.client.get_me()
            if iq.id == pika_id1:
                ax[0]
                _alert_ = "Hi My Peru Master's bot here ,\n\nWhy r u clicking this this.Please get your own PikaBot, and don't use mine!"
                await pika_.answer(_alert_, cache_time=0, alert=True)

    @tgbot.on(Pika_CallBack(data=re.compile(b"pikab(.*)")))
    async def _pikacallback(pika_):
        _pikaa_ = (pika_.query).user_id
        if (
            _pikaa_ == pika_id1
            or _pikaa_ == pika_id2
            or _pikaa_ == pika_id3
            or _pikaa_ == pika_id4
        ):
            _pika = f"""Pïkå¢hµ Úsêrßð† {helpstr}"""
            _pikacmds = bot.pika_cmd
            _pika += "\n**Currently Loaded Plugins**: {}".format(
                len(_pikacmds))
            _pika_ = paginate_help(0, _pikacmds, "helpme")
            await pika_.edit(_pika, buttons=_pika_, link_preview=False)
        else:
            _alert_ = "Please get your own PikaBot, and don't use mine!"
            await pika_.answer(_alert_, cache_time=0, alert=True)

    @tgbot.on(Pika_CallBack(data=re.compile(b"tools(.*)")))
    async def _pikacallback(pika_):
        _pikaa_ = (pika_.query).user_id
        if (
            _pikaa_ == pika_id1
            or _pikaa_ == pika_id2
            or _pikaa_ == pika_id3
            or _pikaa_ == pika_id4
        ):

            a = randint(0, 9)
            _rx_ = f"{_emo_[a]}" + f" {rx}"
            _pikacmds = bot.pika_cmd
            pika_.data_match.group(1).decode("UTF-8")
            _pika = _pikacmds["systools"].__doc__.format(i=_rx_)
            _pikaB = [(custom.Button.inline("⫷BacK", data="pikab"))]
            await pika_.edit(_pika, buttons=_pikaB)


@tgbot.on(Pika_CallBack(data=re.compile(rb"pika1\((.+?)\)")))
async def _(_pika):
    pikacmds = tgbot.PikaAsst
    c_p_n = int(_pika.data_match.group(1).decode("UTF-8"))
    buttons = assistent_help(c_p_n + 1, pikacmds, "helpme")
    await pika_.edit(buttons=buttons)


@tgbot.on(Pika_CallBack(data=re.compile(rb"pika2\((.+?)\)")))
async def _(pika_):
    pikacmds = tgbot.PikaAsst
    c_p_n = int(pika_.data_match.group(1).decode("UTF-8"))
    buttons = assistent_help(
        c_p_n - 1,
        pikacmds,
        "helpme")  # pylint:disable=E0602
    await pika_.edit(buttons=buttons)


@tgbot.on(Pika_CallBack(data=re.compile(b"pika3")))
async def _(pika_):
    await pika_.edit("Pika Pi! Restarting wait for 1 Min!")
    await asyncio.sleep(4)
    await pika_.delete()
    pika_start()


@tgbot.on(Pika_CallBack(data=re.compile(b"pika4")))
async def _(pika_):
    _a_ = await pika_.edit("Pika Pi! Menu Closed!")
    await asyncio.sleep(3)
    await _a_.delete()


@tgbot.on(Pika_CallBack(data=re.compile(b"pika5(.*)")))
async def _(pika_):
    a = randint(0, 9)
    _rx_ = f"{_emo_[a]}" + f" {rx}"
    _pikacmds = tgbot.PikaAsst
    _pika_ = pika_.data_match.group(1).decode("UTF-8")
    _pika = _pikacmds[_pika_].__doc__.format(i=_rx_)
    _pikaB = [(custom.Button.inline("⫷BacK", data="pika6"))]
    await pika_.edit(_pika, buttons=_pikaB)


@tgbot.on(Pika_CallBack(data=re.compile(b"pika6(.*)")))
async def _(pika_):
    _pika = f"""Pïkå¢hµ Úsêrßð† {helpstr}"""
    _pikacmds = tgbot.PikaAsst
    _pika += "\n**Currently Loaded Plugins**: {}".format(len(_pikacmds))
    _pika_ = assistent_help(0, _pikacmds, "helpme")
    await pika_.edit(_pika, buttons=_pika_, link_preview=False)


def assistent_help(page_number, loaded_plugins, prefix):

    number_of_rows = pikrws
    number_of_cols = pikcl
    helpable_plugins = []
    for p in loaded_plugins:
        if not p.startswith("_"):
            helpable_plugins.append(p)

    helpable_plugins = sorted(helpable_plugins)

    _data1 = f"pika5{const}"
    _data2 = f"{const}pika1({const})"
    _data3 = f"{const}pika2({const})"

    modules = [
        custom.Button.inline("{} {} {}".format(xl, x, xl), data=_data1.format(x))
        for x in helpable_plugins
    ]
    if number_of_cols == 1:
        pairs = list(zip(modules[::number_of_cols]))
    elif number_of_cols == 2:
        pairs = list(zip(modules[::number_of_cols],
                     modules[1::number_of_cols]))
    elif number_of_cols == 3:
        pairs = list(
            zip(
                modules[::number_of_cols],
                modules[1::number_of_cols],
                modules[2::number_of_cols],
            )
        )
    elif number_of_cols == 4:
        pairs = list(
            zip(
                modules[::number_of_cols],
                modules[1::number_of_cols],
                modules[2::number_of_cols],
                modules[3::number_of_cols],
            )
        )
    else:
        pairs = list(
            zip(
                modules[::number_of_cols],
                modules[1::number_of_cols],
                modules[2::number_of_cols],
                modules[3::number_of_cols],
            )
        )
    max_num_pages = math.ceil(len(pairs) / number_of_rows)
    modulo_page = page_number % max_num_pages
    if len(pairs) > number_of_rows:
        pairs = (
            [
                (
                    custom.Button.inline("«]", data=_data2.format(prefix, modulo_page)),
                    custom.Button.inline("Close🙅‍♀️", data="close"),
                    custom.Button.inline("[»", data=_data3.format(prefix, modulo_page)),
                )
            ]
            + pairs[modulo_page * number_of_rows: number_of_rows * (modulo_page + 1)]
            + [(custom.Button.inline("🤖Restart Me", data="restart"),)]
            + [(custom.Button.inline("⚔️Tools", data="tools"),)]
        )

    return pairs


def paginate_help(page_number, loaded_plugins, prefix):

    number_of_rows = pikrws
    number_of_cols = pikcl
    helpable_plugins = []
    for p in loaded_plugins:
        if not p.startswith("_"):
            helpable_plugins.append(p)

    helpable_plugins = sorted(helpable_plugins)
    if loaded_plugins == bot.pika_cmd:
        _data1 = f"us_plugin_{const}"
        _data2 = f"{const}_prev({const})"
        _data3 = f"{const}_next({const})"
    else:
        _data1 = f"pika5{const}"
        _data2 = f"{const}pika1({const})"
        _data3 = f"{const}pika2({const})"

    modules = [
        custom.Button.inline("{} {} {}".format(xl, x, xl), data=_data1.format(x))
        for x in helpable_plugins
    ]
    if number_of_cols == 1:
        pairs = list(zip(modules[::number_of_cols]))
    elif number_of_cols == 2:
        pairs = list(zip(modules[::number_of_cols],
                     modules[1::number_of_cols]))
    elif number_of_cols == 3:
        pairs = list(
            zip(
                modules[::number_of_cols],
                modules[1::number_of_cols],
                modules[2::number_of_cols],
            )
        )
    elif number_of_cols == 4:
        pairs = list(
            zip(
                modules[::number_of_cols],
                modules[1::number_of_cols],
                modules[2::number_of_cols],
                modules[3::number_of_cols],
            )
        )
    else:
        pairs = list(
            zip(
                modules[::number_of_cols],
                modules[1::number_of_cols],
                modules[2::number_of_cols],
                modules[3::number_of_cols],
            )
        )
    max_num_pages = math.ceil(len(pairs) / number_of_rows)
    modulo_page = page_number % max_num_pages
    if len(pairs) > number_of_rows:
        pairs = (
            [
                (
                    custom.Button.inline("«]", data=_data2.format(prefix, modulo_page)),
                    custom.Button.inline("Close🙅‍♀️", data="close"),
                    custom.Button.inline("[»", data=_data3.format(prefix, modulo_page)),
                )
            ]
            + pairs[modulo_page * number_of_rows: number_of_rows * (modulo_page + 1)]
            + [(custom.Button.inline("🤖Restart Me", data="restart"),)]
            + [(custom.Button.inline("⚔️Tools", data="tools"),)]
        )

    return pairs


async def _currency(event):
    if event.fwd_from:
        return
    start = pikatime.now()
    input_str = event.pattern_match.group(1)
    input_sgra = input_str.split(" ")
    if len(input_sgra) == 3:
        try:
            number = float(input_sgra[0])
            currency_from = input_sgra[1].upper()
            currency_to = input_sgra[2].upper()
            request_url = "https://api.exchangeratesapi.io/latest?base={}".format(
                currency_from)
            current_response = requests.get(request_url).json()
            if currency_to in current_response["rates"]:
                current_rate = float(current_response["rates"][currency_to])
                rebmun = round(number * current_rate, 2)
                await event.edit(
                    "{} {} = {} {}".format(number, currency_from, rebmun, currency_to)
                )
            else:
                await event.edit("IDEKNOWTDWTT")
        except e:
            await event.edit(str(e))
    else:
        await event.edit("`.currency number from to`")
    end = pikatime.now()
    (end - start).seconds


async def _figlet(event):
    if event.fwd_from:
        return
    CMD_FIG = {
        "slant": "slant",
        "3D": "3-d",
        "5line": "5lineoblique",
        "alpha": "alphabet",
        "banner": "banner3-D",
        "doh": "doh",
        "iso": "isometric1",
        "letter": "letters",
        "allig": "alligator",
        "dotm": "dotmatrix",
        "bubble": "bubble",
        "bulb": "bulbhead",
        "digi": "digital",
    }
    input_str = event.pattern_match.group(1)
    if "|" in input_str:
        text, cmd = input_str.split("|", maxsplit=1)
    elif input_str is not None:
        cmd = None
        text = input_str
    else:
        await event.edit("Please add some text to figlet")
        return
    if cmd is not None:
        try:
            font = CMD_FIG[cmd]
        except KeyError:
            await event.edit("Invalid selected font.")
            return
        result = pyfiglet.figlet_format(text, font=font)
    else:
        result = pyfiglet.figlet_format(text)
    await event.respond("‌‌‎`{}`".format(result))
    await event.delete()


async def _getfilext(event):
    if event.fwd_from:
        return
    await event.edit("Processing ...")
    sample_url = "https://www.fileext.com/file-extension/{}.html"
    input_str = event.pattern_match.group(1).lower()
    response_api = requests.get(sample_url.format(input_str))
    status_code = response_api.status_code
    if status_code == 200:
        raw_html = response_api.content
        soup = BeautifulSoup(raw_html, "html.parser")
        ext_details = soup.find_all("td", {"colspan": "3"})[-1].text
        await event.edit(
            "**File Extension**: `{}`\n**Description**: `{}`".format(
                input_str, ext_details
            )
        )
    else:
        await event.edit(
            "https://www.fileext.com/ responded with {} for query: {}".format(
                status_code, input_str
            )
        )


async def _fleave(event):
    if event.fwd_from:

        return

    animation_interval = 1

    animation_ttl = range(0, 17)

    # input_str = event.pattern_match.group(1)

    # if input_str == "fleave":

    await event.edit("fleave")

    animation_chars = [
        "⬛⬛⬛\n⬛⬛⬛\n⬛⬛⬛",
        "⬛⬛⬛\n⬛🔄⬛\n⬛⬛⬛",
        "⬛⬆️⬛\n⬛🔄⬛\n⬛⬛⬛",
        "⬛⬆️↗️\n⬛🔄⬛\n⬛⬛⬛",
        "⬛⬆️↗️\n⬛🔄➡️\n⬛⬛⬛",
        "⬛⬆️↗️\n⬛🔄➡️\n⬛⬛↘️",
        "⬛⬆️↗️\n⬛🔄➡️\n⬛⬇️↘️",
        "⬛⬆️↗️\n⬛🔄➡️\n↙️⬇️↘️",
        "⬛⬆️↗️\n⬅️🔄➡️\n↙️⬇️↘️",
        "↖️⬆️↗️\n⬅️🔄➡️\n↙️⬇️↘️",
        "**Chat Message Exported To** `./Inpu/`",
        "**Chat Message Exported To** `./Inpu/homework/`",
        "**Chat Message Exported To** `./Inpu/homework/groupchat.txt`",
        "__Legend is leaving this chat.....! ",
        "__Legend is leaving this chat.....!",
    ]

    for i in animation_ttl:

        await asyncio.sleep(animation_interval)

        await event.edit(animation_chars[i % 17])


async def _ftext(event):
    input_str = event.pattern_match.group(1)
    if input_str:
        paytext = input_str
        pay = "{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}".format(
            paytext * 8,
            paytext * 8,
            paytext * 2,
            paytext * 2,
            paytext * 2,
            paytext * 6,
            paytext * 6,
            paytext * 2,
            paytext * 2,
            paytext * 2,
            paytext * 2,
            paytext * 2,
        )
    else:
        pay = "╭━━━╮\n┃╭━━╯\n┃╰━━╮\n┃╭━━╯\n┃┃\n╰╯\n"
    # pay = "{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}".format(paytext*8, paytext*8, paytext*2, paytext*2, paytext*2, paytext*6, paytext*6, paytext*2, paytext*2, paytext*2, paytext*2, paytext*2)
    await event.edit(pay)


async def _fuck(event):
    if event.fwd_from:
        return
    animation_interval = 1
    animation_ttl = range(0, 101)
    input_str = event.pattern_match.group(1)
    if input_str == "fuck":
        await event.edit("fuck")
        animation_chars = ["👉       ✊️", "👉     ✊️", "👉  ✊️", "👉✊️💦"]
        for i in animation_ttl:
            await asyncio.sleep(animation_interval)
            await event.edit(animation_chars[i % 4])

    if input_str == "kiss":
        await event.edit("kiss")
        animation_chars = ["🤵       👰", "🤵     👰", "🤵  👰", "🤵💋👰"]
        for i in animation_ttl:
            await asyncio.sleep(animation_interval)
            await event.edit(animation_chars[i % 4])

    if input_str == "sux":
        await event.edit("sux")
        animation_chars = ["🤵       👰", "🤵     👰", "🤵  👰", "🤵👼👰"]
        for i in animation_ttl:
            await asyncio.sleep(animation_interval)
            await event.edit(animation_chars[i % 4])


async def _fwd(event):
    if event.fwd_from:
        return
    if Config.BOTLOG_CHATID is None:
        await event.edit(
            "Please set the required environment variable `BOTLOG_CHATID` for this plugin to work"
        )
    else:
        re_message = await event.get_reply_message()
        # https://t.me/telethonofftopic/78166
        fwd_message = await event.client.forward_messages(e, re_message, silent=True)
        await event.client.forward_messages(event.chat_id, fwd_message)
        await fwd_message.delete()
        await event.delete()


async def _gbot(event):
    if event.fwd_from:
        return
    mentions = "**🤖Bots in this Chat**: \n"
    input_str = event.pattern_match.group(1)
    to_write_chat = await event.get_input_chat()
    chat = None
    if not input_str:
        chat = to_write_chat
    else:
        mentions = "🤖Bots in {} : \n".format(input_str)
        try:
            chat = await event.client.get_entity(input_str)
        except Exception as e:
            await event.edit(str(e))
            return None
    try:
        async for x in event.client.iter_participants(
            chat, filter=ChannelParticipantsBots
        ):
            if isinstance(x.participant, ChannelParticipantAdmin):
                mentions += "\n 🔥 [{}](tg://user?id={}) `{}`".format(
                    x.first_name, x.id, x.id
                )
            else:
                mentions += "\n [{}](tg://user?id={}) `{}`".format(
                    x.first_name, x.id, x.id
                )
    except Exception as e:
        mentions += " " + str(e) + "\n"
    await event.edit(mentions)


async def _gadmins(event):
    if event.fwd_from:
        return
    mentions = "**Admins in this Channel**: \n"
    should_mention_admins = False
    reply_message = None
    pattern_match_str = event.pattern_match.group(1)
    if "m" in pattern_match_str:
        should_mention_admins = True
        if event.reply_to_msg_id:
            reply_message = await event.get_reply_message()
    input_str = event.pattern_match.group(2)
    to_write_chat = await event.get_input_chat()
    chat = None
    if not input_str:
        chat = to_write_chat
    else:
        mentions_heading = "Admins in {} channel: \n".format(input_str)
        mentions = mentions_heading
        try:
            chat = await event.client.get_entity(input_str)
        except Exception as e:
            await event.edit(str(e))
            return None
    try:
        async for x in event.client.iter_participants(
            chat, filter=ChannelParticipantsAdmins
        ):
            if not x.deleted:
                if isinstance(x.participant, ChannelParticipantCreator):
                    mentions += "\n 🔱 [{}](tg://user?id={}) `{}`".format(
                        x.first_name, x.id, x.id
                    )
        mentions += "\n"
        async for x in event.client.iter_participants(
            chat, filter=ChannelParticipantsAdmins
        ):
            if not x.deleted:
                if isinstance(x.participant, ChannelParticipantAdmin):
                    mentions += "\n 🥇 [{}](tg://user?id={}) `{}`".format(
                        x.first_name, x.id, x.id
                    )
            else:
                mentions += "\n `{}`".format(x.id)
    except Exception as e:
        mentions += " " + str(e) + "\n"
    if should_mention_admins:
        if reply_message:
            await reply_message.reply(mentions)
        else:
            await event.reply(mentions)
        await event.delete()
    else:
        await event.edit(mentions)


async def _getid(event):
    if event.fwd_from:
        return
    _tg = await get_pika_tg(event)
    a = await pika_msg(event, "Getting info, Please wait...", _tg)
    if event.reply_to_msg_id:
        await event.get_input_chat()
        r_msg = await event.get_reply_message()
        if r_msg.media:
            bot_api_file_id = pack_bot_file_id(r_msg.media)
            await pika_msg(
                a,
                "Current Chat ID: `{}`\nFrom User ID: `{}`\nBot API File ID: `{}`".format(
                    str(event.chat_id), str(r_msg.sender_id), bot_api_file_id
                ),
            )
        else:
            await pika_msg(
                a,
                "Current Chat ID: `{}`\nFrom User ID: `{}`".format(
                    str(event.chat_id), str(r_msg.sender_id)
                ),
            )
    else:
        await pika_msg(a, "Current Chat ID: `{}`".format(str(event.chat_id)))


async def _gps(event):
    if event.fwd_from:
        return
    reply_to_id = event.message
    if event.reply_to_msg_id:
        reply_to_id = await event.get_reply_message()
    input_str = event.pattern_match.group(1)

    if not input_str:
        return await event.edit("Boss ! Give A Place To Search 😔 !.")

    await event.edit("Finding This Location In Maps Server.....")

    geolocator = Nominatim(user_agent="Pikachu Userbot")
    geoloc = geolocator.geocode(input_str)

    if geoloc:
        lon = geoloc.longitude
        lat = geoloc.latitude
        await reply_to_id.reply(
            input_str, file=types.InputMediaGeoPoint(types.InputGeoPoint(lat, lon))
        )
        await event.delete()
    else:
        await event.edit("i coudn't find it")


async def _ggl(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    sample_url = "https://da.gd/s?url=https://lmgtfy.com/?q={}%26iie=1".format(
        input_str.replace(" ", "+")
    )
    response_api = requests.get(sample_url).text
    if response_api:
        await event.edit(
            "[{}]({})\n`Thank me Later 🙃` ".format(input_str, response_api.rstrip())
        )
    else:
        await event.edit("something is wrong. please try again later.")


async def _invite(event):
    if event.fwd_from:
        return
    to_add_users = event.pattern_match.group(1)
    if event.is_private:
        await event.edit("`.invite` users to a chat, not to a Private Message")
    else:
        pikalog.info(to_add_users)
        if not event.is_channel and event.is_group:
            # https://lonamiwebs.github.io/Telethon/methods/messages/add_chat_user.html
            for user_id in to_add_users.split(" "):
                try:
                    await event.client(
                        functions.messages.AddChatUserRequest(
                            chat_id=event.chat_id, user_id=user_id, fwd_limit=1000000
                        )
                    )
                except Exception as e:
                    await event.reply(str(e))
            await event.edit("Invited Successfully")
        else:
            # https://lonamiwebs.github.io/Telethon/methods/channels/invite_to_channel.html
            for user_id in to_add_users.split(" "):
                try:
                    await event.client(
                        functions.channels.InviteToChannelRequest(
                            channel=event.chat_id, users=[user_id]
                        )
                    )
                except Exception as e:
                    await event.reply(str(e))
            await event.edit("Invited Successfully")


async def _github(event):
    if event.fwd_from:
        return
    _tg = await get_pika_tg(event)
    input_str = event.pattern_match.group(1)
    a = await pika_msg(event, "Searching for {}".format(input_str), _tg)
    await asyncio.sleep(2)
    url = "https://api.github.com/users/{}".format(input_str)
    r = requests.get(url)
    if r.status_code != 404:
        b = r.json()
        avatar_url = b["avatar_url"]
        html_url = b["html_url"]
        gh_type = b["type"]
        name = b["name"]
        company = b["company"]
        blog = b["blog"]
        location = b["location"]
        bio = b["bio"]
        created_at = b["created_at"]
        await event.client.send_file(
            event.chat_id,
            caption="""Name: [{}]({})
Type: {}
Company: {}
Blog: {}
Location: {}
Bio: {}
Profile Created: {}""".format(
                name, html_url, gh_type, company, blog, location, bio, created_at
            ),
            file=avatar_url,
            force_document=False,
            allow_cache=False,
            reply_to=event,
        )
        await a.delete()
    else:
        await pika_msg(a, "`{}`: {}".format(input_str, r.text))


async def _gsearch(event):
    """ For .google command, do a Google search. """
    match = event.pattern_match.group(1)
    _tg = await get_pika_tg(event)
    page = findall(r"page=\d+", match)
    a = await pika_msg(event, f"Searching for {match}", _tg)
    try:
        page = page[0]
        page = page.replace("page=", "")
        match = match.replace("page=" + page[0], "")
    except IndexError:
        page = 1
    search_args = (str(match), int(page))
    gsearch = GoogleSearch()
    gresults = await gsearch.async_search(*search_args)
    msg = ""
    for i in range(len(gresults["links"])):
        try:
            title = gresults["titles"][i]
            link = gresults["links"][i]
            desc = gresults["descriptions"][i]
            msg += f"[{title}]({link})\n`{desc}`\n\n"
        except IndexError:
            break
    finalres = "**Search Query:**\n`" + match + "`\n\n**Results:**\n" + msg
    await pika_msg(a, finalres, link_preview=False)


langi = "en"


async def _imdb(e):
    _tg = await get_pika_tg(e)
    try:
        movie_name = e.pattern_match.group(1)
        remove_space = movie_name.split(" ")
        _ax = await pika_msg(e, f"Searching For {movie_name}, Please wait...", _tg)
        final_name = "+".join(remove_space)
        page = requests.get(
            "https://www.imdb.com/find?ref_=nv_sr_fn&q=" +
            final_name +
            "&s=all")
        str(page.status_code)
        soup = bs4.BeautifulSoup(page.content, "lxml")
        odds = soup.findAll("tr", "odd")
        mov_title = odds[0].findNext("td").findNext("td").text
        mov_link = ("http://www.imdb.com/" +
                    odds[0].findNext("td").findNext("td").a["href"])
        page1 = requests.get(mov_link)
        soup = bs4.BeautifulSoup(page1.content, "lxml")
        if soup.find("div", "poster"):
            poster = soup.find("div", "poster").img["src"]
        else:
            poster = ""
        if soup.find("div", "title_wrapper"):
            pg = soup.find("div", "title_wrapper").findNext("div").text
            mov_details = re.sub(r"\s+", " ", pg)
        else:
            mov_details = ""
        credits = soup.findAll("div", "credit_summary_item")
        if len(credits) == 1:
            director = credits[0].a.text
            writer = "Not available"
            stars = "Not available"
        elif len(credits) > 2:
            director = credits[0].a.text
            writer = credits[1].a.text
            actors = []
            for x in credits[2].findAll("a"):
                actors.append(x.text)
            actors.pop()
            stars = actors[0] + "," + actors[1] + "," + actors[2]
        else:
            director = credits[0].a.text
            writer = "Not available"
            actors = []
            for x in credits[1].findAll("a"):
                actors.append(x.text)
            actors.pop()
            stars = actors[0] + "," + actors[1] + "," + actors[2]
        if soup.find("div", "inline canwrap"):
            story_line = soup.find(
                "div", "inline canwrap").findAll("p")[0].text
        else:
            story_line = "Not available"
        info = soup.findAll("div", "txt-block")
        if info:
            mov_country = []
            mov_language = []
            for node in info:
                a = node.findAll("a")
                for i in a:
                    if "country_of_origin" in i["href"]:
                        mov_country.append(i.text)
                    elif "primary_language" in i["href"]:
                        mov_language.append(i.text)
        if soup.findAll("div", "ratingValue"):
            for r in soup.findAll("div", "ratingValue"):
                mov_rating = r.strong["title"]
        else:
            mov_rating = "Not available"
        imdb_dta = (
            "<a href=" + poster + ">&#8203;</a>"
            "<b>Title : </b><code>"
            + mov_title
            + "</code>\n<code>"
            + mov_details
            + "</code>\n<b>Rating : </b><code>"
            + mov_rating
            + "</code>\n<b>Country : </b><code>"
            + mov_country[0]
            + "</code>\n<b>Language : </b><code>"
            + mov_language[0]
            + "</code>\n<b>Director : </b><code>"
            + director
            + "</code>\n<b>Writer : </b><code>"
            + writer
            + "</code>\n<b>Stars : </b><code>"
            + stars
            + "</code>\n<b>IMDB Url : </b>"
            + mov_link
            + "\n<b>Story Line : </b>"
            + story_line
        )
        _html = "HTML"
        await pika_msg(_ax, imdb_dta, link_preview=True, parse_mode=_html)
    except IndexError:
        await pika_msg(_ax, "Plox enter **Valid movie name** kthx")


async def _getinfo(event):
    if event.fwd_from:
        return
    _tg = await get_pika_tg(event)
    a = await pika_msg(event, "Getting User Info. Please wait....", _tg)
    replied_user, error_i_a = await get_full_user(event)
    if replied_user is None:
        await event.edit(str(error_i_a))
        return False
    replied_user_profile_photos = await event.client(
        GetUserPhotosRequest(
            user_id=replied_user.user.id, offset=42, max_id=0, limit=80
        )
    )
    replied_user_profile_photos_count = "NaN"
    try:
        replied_user_profile_photos_count = replied_user_profile_photos.count
    except AttributeError:
        pass
    user_id = replied_user.user.id
    first_name = html.escape(replied_user.user.first_name)
    if first_name is not None:
        first_name = first_name.replace("\u2060", "")
    last_name = replied_user.user.last_name
    last_name = (last_name.replace("\u2060", "")
                 if last_name else ("Last Name not found"))
    user_bio = replied_user.about
    if user_bio is not None:
        user_bio = html.escape(replied_user.about)
    common_chats = replied_user.common_chats_count
    try:
        dc_id, location = get_input_location(replied_user.profile_photo)
    except Exception as e:
        dc_id = "`Need a Profile Picture to check **this**`"
        str(e)
    caption = """<b>Extracted UserInfo From Telegram Database By PikaBot<b>
<b>🔥Telegram ID</b>: <code>{}</code>
<b>🤟Permanent Link</b>: <a href='tg://user?id={}'>Click Here</a>
<b>🗣️First Name</b>: <code>{}</code>
<b>🗣️Second Name</b>: <code>{}</code>
<b>👨🏿‍💻BIO</b>: {}
<b>🎃DC ID</b>: {}
<b>⚡NO OF PSS</b> : {}
<b>🤔IS RESTRICTED</b>: {}
<b>✅VERIFIED</b>: {}
<b>🙄IS A BOT</b>: {}
<b>👥Groups in Common</b>: {}
""".format(
        user_id,
        user_id,
        first_name,
        last_name,
        user_bio,
        dc_id,
        replied_user_profile_photos_count,
        replied_user.user.restricted,
        replied_user.user.verified,
        replied_user.user.bot,
        common_chats,
    )
    message_id_to_reply = event.message.reply_to_msg_id
    if not message_id_to_reply:
        message_id_to_reply = event.message.id
    await event.client.send_message(
        event.chat_id,
        caption,
        reply_to=message_id_to_reply,
        parse_mode="HTML",
        file=replied_user.profile_photo,
        force_document=False,
        silent=True,
    )
    await a.delete()


async def get_full_user(event):
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        if previous_message.forward:
            replied_user = await event.client(
                GetFullUserRequest(
                    previous_message.forward.sender_id
                    or previous_message.forward.channel_id
                )
            )
            return replied_user, None
        else:
            replied_user = await event.client(
                GetFullUserRequest(previous_message.sender_id)
            )
            return replied_user, None
    else:
        input_str = None
        try:
            input_str = event.pattern_match.group(1)
        except IndexError as e:
            return None, e
        if event.message.entities is not None:
            mention_entity = event.message.entities
            probable_user_mention_entity = mention_entity[0]
            if isinstance(
                    probable_user_mention_entity,
                    MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                replied_user = await event.client(GetFullUserRequest(user_id))
                return replied_user, None
            else:
                try:
                    user_object = await event.client.get_entity(input_str)
                    user_id = user_object.id
                    replied_user = await event.client(GetFullUserRequest(user_id))
                    return replied_user, None
                except Exception as e:
                    return None, e
        elif event.is_private:
            try:
                user_id = event.chat_id
                replied_user = await event.client(GetFullUserRequest(user_id))
                return replied_user, None
            except Exception as e:
                return None, e
        else:
            try:
                user_object = await event.client.get_entity(int(input_str))
                user_id = user_object.id
                replied_user = await event.client(GetFullUserRequest(user_id))
                return replied_user, None
            except Exception as e:
                return None, e


async def _json(event):
    if event.fwd_from:
        return
    _tg = await is_pikatg(event)
    a = await pika_msg(event, "Getting message info. Please wait...", _tg)
    await asyncio.sleep(2)
    the_real_message = None
    reply_to_id = None
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        the_real_message = previous_message.stringify()
        reply_to_id = event.reply_to_msg_id
    else:
        the_real_message = event.stringify()
        reply_to_id = event.message.id
    if len(the_real_message) > Config.MAX_MESSAGE_SIZE_LIMIT:
        with io.BytesIO(str.encode(the_real_message)) as out_file:
            out_file.name = "json.text"
            await event.client.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                reply_to=reply_to_id,
            )
            await a.delete()
    else:
        await pika_msg(a, "`{}`".format(the_real_message))


async def _locks(event):
    input_str = event.pattern_match.group(1).lower()
    _tg = await get_pika_tg(event)
    await pika_msg(event, f"Locking {input_str}, Please Wait....", _tg)
    peer_id = event.chat_id
    msg = None
    media = None
    sticker = None
    gif = None
    gamee = None
    ainline = None
    gpoll = None
    adduser = None
    cpin = None
    changeinfo = None
    if input_str == "msg":
        msg = True
        what = "messages"
    elif input_str == "media":
        media = True
        what = "media"
    elif input_str == "sticker":
        sticker = True
        what = "stickers"
    elif input_str == "gif":
        gif = True
        what = "GIFs"
    elif input_str == "game":
        gamee = True
        what = "games"
    elif input_str == "inline":
        ainline = True
        what = "inline bots"
    elif input_str == "poll":
        gpoll = True
        what = "polls"
    elif input_str == "invite":
        adduser = True
        what = "invites"
    elif input_str == "pin":
        cpin = True
        what = "pins"
    elif input_str == "info":
        changeinfo = True
        what = "chat info"
    elif input_str == "all":
        msg = True
        media = True
        sticker = True
        gif = True
        gamee = True
        ainline = True
        gpoll = True
        adduser = True
        cpin = True
        changeinfo = True
        what = "everything"
    else:
        if not input_str:
            await pika_msg(a, "`I can't lock nothing !!`")
            return
        else:
            await pika_msg(a, f"`Invalid lock type:` {input_str}")
            return

    lock_rights = ChatBannedRights(
        until_date=None,
        send_messages=msg,
        send_media=media,
        send_stickers=sticker,
        send_gifs=gif,
        send_games=gamee,
        send_inline=ainline,
        send_polls=gpoll,
        invite_users=adduser,
        pin_messages=cpin,
        change_info=changeinfo,
    )
    try:
        await event.client(
            EditChatDefaultBannedRightsRequest(peer=peer_id, banned_rights=lock_rights)
        )
        await pika_msg(a, f"`locked {what} Because its Rest Time Nimba!!`")
    except BaseException as e:
        await pika_msg(a, f"`Do I have proper rights for that ??`\n**Error:** {str(e)}")
        return


async def _rmlocks(event):
    input_str = event.pattern_match.group(1).lower()
    _tg = await get_pika_tg(event)
    a = await pika_msg(event, f"Unlocking {input_str}, Please Wait....", _tg)
    peer_id = event.chat_id
    msg = None
    media = None
    sticker = None
    gif = None
    gamee = None
    ainline = None
    gpoll = None
    adduser = None
    cpin = None
    changeinfo = None
    if input_str == "msg":
        msg = False
        what = "messages"
    elif input_str == "media":
        media = False
        what = "media"
    elif input_str == "sticker":
        sticker = False
        what = "stickers"
    elif input_str == "gif":
        gif = False
        what = "GIFs"
    elif input_str == "game":
        gamee = False
        what = "games"
    elif input_str == "inline":
        ainline = False
        what = "inline bots"
    elif input_str == "poll":
        gpoll = False
        what = "polls"
    elif input_str == "invite":
        adduser = False
        what = "invites"
    elif input_str == "pin":
        cpin = False
        what = "pins"
    elif input_str == "info":
        changeinfo = False
        what = "chat info"
    elif input_str == "all":
        msg = False
        media = False
        sticker = False
        gif = False
        gamee = False
        ainline = False
        gpoll = False
        adduser = False
        cpin = False
        changeinfo = False
        what = "everything"
    else:
        if not input_str:
            await pika_msg(a, "`I can't unlock nothing !!`")
            return
        else:
            await pika_msg(a, f"`Invalid unlock type:` {input_str}")
            return

    unlock_rights = ChatBannedRights(
        until_date=None,
        send_messages=msg,
        send_media=media,
        send_stickers=sticker,
        send_gifs=gif,
        send_games=gamee,
        send_inline=ainline,
        send_polls=gpoll,
        invite_users=adduser,
        pin_messages=cpin,
        change_info=changeinfo,
    )
    try:
        await event.client(
            EditChatDefaultBannedRightsRequest(
                peer=peer_id, banned_rights=unlock_rights
            )
        )
        await pika_msg(a, f"`Unlocked {what} now Start Chit Chat !!`")
    except BaseException as e:
        await pika_msg(a, f"`Do I have proper rights for that ??`\n**Error:** {str(e)}")
        return


async def _pack(event):
    a = await event.get_reply_message()
    input_str = event.pattern_match.group(1)
    b = open(input_str, "w")
    b.write(str(a.message))
    b.close()
    _tg = await get_pika_tg(event)
    _a = await pika_msg(event, f"**Packing into** `{input_str}`", _tg)
    await asyncio.sleep(2)
    await pika_msg(_a, f"**Uploading** `{input_str}`")
    await asyncio.sleep(1)
    await event.client.send_file(
        event.chat_id, input_str, caption="Here is your {}".format(input_str)
    )
    await event.delete()
    os.remove(input_str)


def progress(current, total):
    pikalog.info(
        "Downloaded {} of {}\nCompleted {}".format(
            current, total, (current / total) * 100
        )
    )


async def _deldog(event):
    if event.fwd_from:
        return
    _tg = await get_pika_tg(event)
    a = await pika_msg(event, "Pasting on Deldog, Please wait...", _tg)
    await asyncio.sleep(1)
    start = pikatime.now()
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    input_str = event.pattern_match.group(1)
    message = "SYNTAX: `.paste <long text to include>`"
    if input_str:
        message = input_str
    elif event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        if previous_message.media:
            downloaded_file_name = await event.client.download_media(
                previous_message,
                Config.TMP_DOWNLOAD_DIRECTORY,
                progress_callback=progress,
            )
            m_list = None
            with open(downloaded_file_name, "rb") as fd:
                m_list = fd.readlines()
            message = ""
            for m in m_list:
                message += m.decode("UTF-8") + "\r\n"
            os.remove(downloaded_file_name)
        else:
            message = previous_message.message
    else:
        message = "SYNTAX: `.paste <long text to include>`"
    url = "https://del.dog/documents"
    r = requests.post(url, data=message.encode("UTF-8")).json()
    url = f"https://del.dog/{r['key']}"
    end = pikatime.now()
    ms = (end - start).seconds
    if r["isUrl"]:
        nurl = f"https://del.dog/v/{r['key']}"
        await pika_msg(
            a, "Dogged to {} in {} seconds. GoTo Original URL: {}".format(url, ms, nurl)
        )
    else:
        await pika_msg(a, "Deldog: [Here]({})\n**Time Taken**: {}sec".format(url, ms))


# © @Buddhhu , dont remove credits bsdk else u gay * 100
async def _ncode(event):
    input = event.pattern_match.group(1)
    _tg = await get_pika_tg(event)
    a_ = await pika_msg(
        event, "Converting file into beautified code image, Please wait...", _tg
    )
    a = await event.client.download_media(
        await event.get_reply_message(), Var.TEMP_DOWNLOAD_DIRECTORY
    )
    s = open(a, "r")
    c = s.read()
    s.close()
    pygments.highlight(
        f"{c}",
        Python3Lexer(),
        ImageFormatter(font_name="DejaVu Sans Mono", line_numbers=True),
        "out.png",
    )
    if input == "doc":
        await event.client.send_file(event.chat_id, "out.png", force_document=True)
    else:
        await event.client.send_file(event.chat_id, "out.png")
    await a_.delete()
    os.remove(a)
    os.remove("out.png")


# © @ItzSjDude , dont remove credits bsdk else u gay * 100


async def _reveal(event):
    b = await event.client.download_media(await event.get_reply_message())
    a = open(b, "r")
    c = a.read()
    a.close()
    _tg = await get_pika_tg(event)
    _a = await pika_msg(event, "**Reading file...**", _tg)
    if len(c) > 4095:
        await pika_msg(
            _a, "`The Total words in this file is more than telegram limits.`"
        )
    else:
        await event.client.send_message(event.chat_id, f"```{c}```")
        await _a.delete()
    os.remove(b)
    await _a.delete()


async def _rmbg(event):
    HELP_STR = (
        "`.rmbg` as reply to a media, or give a link as an argument to this command"
    )
    if event.fwd_from:
        return
    if Var.REM_BG_API_KEY is None:
        await event.edit("You need API token from remove.bg to use this plugin.")
        return False
    input_str = event.pattern_match.group(1)
    start = pikatime.now()
    message_id = event.message.id
    _tg = await get_pika_tg(event)
    a = await pika_msg(
        event, "Processing image for background Removal, Please wait...", _tg
    )
    if event.reply_to_msg_id:
        message_id = event.reply_to_msg_id
        reply_message = await event.get_reply_message()
        # check if media message
        try:
            await event.client.download_media(
                reply_message, Config.TMP_DOWNLOAD_DIRECTORY
            )
        except Exception as e:
            await pika_msg(a, str(e))

    if input_str:
        await pika_msg(a, "Sending Image to ReMove.BG, Please wait...")
        output_file_name = ReTrieveURL(input_str)

    if not input_str and event.reply_to_msg_id:
        await pika_msg(a, HELP_STR)

    contentType = output_file_name.headers.get("content-type")
    if "image" in contentType:
        with io.BytesIO(output_file_name.content) as remove_bg_image:
            remove_bg_image.name = "@PikaBot.png"
            await event.client.send_file(
                event.chat_id,
                remove_bg_image,
                force_document=True,
                supports_streaming=False,
                allow_cache=False,
                reply_to=message_id,
            )
        end = pikatime.now()
        ms = (end - start).seconds
        await pika_msg(
            a,
            "Removed dat annoying Backgroup in {} seconds, powered by Pikachu UserBot".format(
                ms
            ),
        )
    if "image" not in contentType:
        await pika_msg(
            a,
            "ReMove.BG API returned Errors. Please report to @ItzSjDudeSupport\n`{}".format(
                output_file_name.content.decode("UTF-8")
            ),
        )


# this method will call the API, and return in the appropriate format
# with the name provided.
def ReTrieveFile(input_file_name):
    headers = {
        "X-API-Key": Var.REM_BG_API_KEY,
    }
    files = {
        "image_file": (input_file_name, open(input_file_name, "rb")),
    }
    r = requests.post(
        "https://api.remove.bg/v1.0/removebg",
        headers=headers,
        files=files,
        allow_redirects=True,
        stream=True,
    )
    return r


def ReTrieveURL(input_url):
    headers = {
        "X-API-Key": Var.REM_BG_API_KEY,
    }
    data = {"image_url": input_url}
    r = requests.post(
        "https://api.remove.bg/v1.0/removebg",
        headers=headers,
        data=data,
        allow_redirects=True,
        stream=True,
    )
    return r


async def _speedtest(event):
    if event.fwd_from:
        return
    _tg = await get_pika_tg(event)
    input_str = event.pattern_match.group(1)
    as_text = True
    as_document = False
    if input_str == "image":
        as_document = False
    elif input_str == "file":
        as_document = True
    elif input_str == "text":
        as_text = True
    a = await pika_msg(event, "`Calculating my internet speed. Please wait!`", _tg)
    start = pikatime.now()
    s = speedtest.Speedtest()
    s.get_best_server()
    s.download()
    s.upload()
    end = pikatime.now()
    ms = (end - start).microseconds / 1000
    response = s.results.dict()
    download_speed = response.get("download")
    upload_speed = response.get("upload")
    ping_time = response.get("ping")
    client_infos = response.get("client")
    i_s_p = client_infos.get("isp")
    i_s_p_rating = client_infos.get("isprating")
    reply_msg_id = event.message.id
    if event.reply_to_msg_id:
        reply_msg_id = event.reply_to_msg_id
    try:
        response = s.results.share()
        speedtest_image = response
        if as_text:
            await pika_msg(
                a,
                """`SpeedTest completed in {} seconds`

`Download: {}`
`Upload: {}`
`Ping: {}`
`Internet Service Provider: {}`
`ISP Rating: {}`""".format(
                    ms,
                    convert_from_bytes(download_speed),
                    convert_from_bytes(upload_speed),
                    ping_time,
                    i_s_p,
                    i_s_p_rating,
                ),
            )
        else:
            await event.client.send_file(
                event.chat_id,
                speedtest_image,
                caption="**SpeedTest** completed in {} seconds".format(ms),
                force_document=as_document,
                reply_to=reply_msg_id,
                allow_cache=False,
            )
            await event.delete()
    except Exception as exc:
        await pika_msg(
            a,
            """**SpeedTest** completed in {} seconds
Download: {}
Upload: {}
Ping: {}

__With the Following ERRORs__
{}""".format(
                ms,
                convert_from_bytes(download_speed),
                convert_from_bytes(upload_speed),
                ping_time,
                str(exc),
            ),
        )


def convert_from_bytes(size):
    power = 2 ** 10
    n = 0
    units = {
        0: "",
        1: "kilobytes",
        2: "megabytes",
        3: "gigabytes",
        4: "terabytes"}
    while size > power:
        size /= power
        n += 1
    return f"{round(size, 2)} {units[n]}"


Heroku = heroku3.from_key(Var.HEROKU_API_KEY)
app = Heroku.app(Var.HEROKU_APP_NAME)


heroku_api = "https://api.heroku.com"


async def _vars(var):
    _tg = await get_pika_tg(var)
    exe = var.pattern_match.group(1)
    heroku_var = app.config()
    if exe == "get":
        a = await pika_msg(var, "`Getting information...`", _tg)
        await asyncio.sleep(1.5)
        try:
            variable = var.pattern_match.group(2).split()[0]
            if variable in heroku_var:
                return await pika_msg(
                    a, "**ConfigVars**:" f"\n\n`{variable} = {heroku_var[variable]}`\n"
                )
            else:
                return await pika_msg(
                    a, "**ConfigVars**:" f"\n\n`Error:\n-> {variable} don't exists`"
                )
        except IndexError:
            configs = prettyjson(heroku_var.to_dict(), indent=2)
            with open("configs.json", "w") as fp:
                fp.write(configs)
            with open("configs.json", "r") as fp:
                result = fp.read()
                if len(result) >= 4096:
                    await var.client.send_file(
                        var.chat_id,
                        "configs.json",
                        reply_to=var.id,
                        caption="`Output too large, sending it as a file`",
                    )
                else:
                    await pika_msg(
                        a,
                        "`[HEROKU]` ConfigVars:\n\n"
                        "================================"
                        f"\n```{result}```\n"
                        "================================",
                    )
            os.remove("configs.json")
            return
    elif exe == "set":
        a = await pika_msg(var, "`Setting information...`", _tg)
        variable = var.pattern_match.group(2)
        if not variable:
            return await pika_msg(a, ">`.set var <ConfigVars-name> <value>`")
        value = var.pattern_match.group(3)
        if not value:
            variable = variable.split()[0]
            try:
                value = var.pattern_match.group(2).split()[1]
            except IndexError:
                return await pika_msg(a, ">`.set var <ConfigVars-name> <value>`")
        await asyncio.sleep(1.5)
        if variable in heroku_var:
            await pika_msg(
                a, f"**{variable}**  `successfully changed to`  ->  **{value}**"
            )
        else:
            await pika_msg(
                a, f"**{variable}**  `successfully added with value`  ->  **{value}**"
            )
        heroku_var[variable] = value
    elif exe == "del":
        a = await pika_msg(var, "`Getting information to deleting variable...`", _tg)
        try:
            variable = var.pattern_match.group(2).split()[0]
        except IndexError:
            return await pika_msg(a, "`Please specify ConfigVars you want to delete`")
        await asyncio.sleep(1.5)
        if variable in heroku_var:
            await pika_msg(a, f"**{variable}**  `successfully deleted`")
            del heroku_var[variable]
        else:
            return await pika_msg(a, f"**{variable}**  `is not exists`")


async def _dyno(dyno):
    """
    Get your account Dyno Usage
    """
    _tg = await get_pika_tg(dyno)
    a = await pika_msg(dyno, "`Calculating your Dyno Usage`", _tg)
    useragent = (
        "Mozilla/5.0 (Linux; Android 10; SM-G975F) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/80.0.3987.149 Mobile Safari/537.36"
    )
    user_id = Heroku.account().id
    headers = {
        "User-Agent": useragent,
        "Authorization": f"Bearer {Var.HEROKU_API_KEY}",
        "Accept": "application/vnd.heroku+json; version=3.account-quotas",
    }
    path = "/accounts/" + user_id + "/actions/get-quota"
    r = requests.get(heroku_api + path, headers=headers)
    if r.status_code != 200:
        return await pika_msg(
            a, "`Error: something bad happened`\n\n" f">.`{r.reason}`\n"
        )
    result = r.json()
    quota = result["account_quota"]
    quota_used = result["quota_used"]

    """ - Used - """
    remaining_quota = quota - quota_used
    percentage = math.floor(remaining_quota / quota * 100)
    minutes_remaining = remaining_quota / 60
    hours = math.floor(minutes_remaining / 60)
    minutes = math.floor(minutes_remaining % 60)

    """ - Current - """
    App = result["apps"]
    try:
        App[0]["quota_used"]
    except IndexError:
        AppQuotaUsed = 0
        AppPercentage = 0
    else:
        AppQuotaUsed = App[0]["quota_used"] / 60
        AppPercentage = math.floor(App[0]["quota_used"] * 100 / quota)
    AppHours = math.floor(AppQuotaUsed / 60)
    AppMinutes = math.floor(AppQuotaUsed % 60)

    await asyncio.sleep(1.5)

    return await pika_msg(
        a,
        "**Dyno Usage**:\n\n"
        f" -> `Dyno usage for`  **{Var.HEROKU_APP_NAME}**:\n"
        f"     •  `{AppHours}`**h**  `{AppMinutes}`**m**  "
        f"**|**  [`{AppPercentage}`**%**]"
        "\n"
        " -> `Dyno hours quota remaining this month`:\n"
        f"     •  `{hours}`**h**  `{minutes}`**m**  "
        f"**|**  [`{percentage}`**%**]",
    )


def prettyjson(obj, indent=2, maxlinelength=80):
    """Renders JSON content with indentation and line splits/concatenations to fit maxlinelength.
    Only dicts, lists and basic types are supported"""

    items, _ = getsubitems(
        obj,
        itemkey="",
        islast=True,
        maxlinelength=maxlinelength - indent,
        indent=indent,
    )
    return indentitems(items, indent, level=0)


async def _restart(rstrt):
    _tg = await get_pika_tg(rstrt)
    await pika_msg(
        rstrt,
        "**Boss I am restarting!, Please wait for a min after that do {x}ping or {x}help**".format(
            x=rx
        ),
        _tg,
    )
    app.restart()


Heroku = heroku3.from_key(Var.HEROKU_API_KEY)
app = Heroku.app(Var.HEROKU_APP_NAME)


async def _logs(dyno):
    _tg = await get_pika_tg(dyno)
    a = await pika_msg(dyno, "Getting Logs....", _tg)
    await asyncio.sleep(1)
    with open("logs.txt", "w") as log:
        log.write(app.get_log())
    await dyno.client.send_file(
        dyno.chat_id,
        "logs.txt",
        reply_to=dyno.id,
        caption="logs of 100+ lines",
    )
    await pika_msg(a, "Sending in Progress.......")
    await asyncio.sleep(1)
    await a.delete()


async def apk(e):
    try:
        app_name = e.pattern_match.group(1)
        remove_space = app_name.split(" ")
        final_name = "+".join(remove_space)
        _tg = await get_pika_tg(e)
        a = await pika_msg(
            e, f"Searching for {app_name} on PlayStore, Please Wait...", _tg
        )
        page = requests.get(
            "https://play.google.com/store/search?q=" + final_name + "&c=apps"
        )
        str(page.status_code)
        soup = bs4.BeautifulSoup(page.content, "lxml", from_encoding="utf-8")
        results = soup.findAll("div", "ZmHEEd")
        app_name = (
            results[0].findNext(
                "div",
                "Vpfmgd").findNext(
                "div",
                "WsMG1c nnK0zc").text)
        app_dev = results[0].findNext(
            "div", "Vpfmgd").findNext(
            "div", "KoLSrc").text
        app_dev_link = (
            "https://play.google.com" +
            results[0].findNext(
                "div",
                "Vpfmgd").findNext(
                "a",
                "mnKHRc")["href"])
        app_rating = (
            results[0]
            .findNext("div", "Vpfmgd")
            .findNext("div", "pf5lIe")
            .find("div")["aria-label"]
        )
        app_link = (
            "https://play.google.com"
            + results[0]
            .findNext("div", "Vpfmgd")
            .findNext("div", "vU6FJ p63iDd")
            .a["href"]
        )
        app_icon = (
            results[0]
            .findNext("div", "Vpfmgd")
            .findNext("div", "uzcko")
            .img["data-src"]
        )
        app_details = "<a href='" + app_icon + "'>📲&#8203;</a>"
        app_details += " <b>" + app_name + "</b>"
        app_details += (
            "\n\n<code>Developer :</code> <a href='"
            + app_dev_link
            + "'>"
            + app_dev
            + "</a>"
        )
        app_details += "\n<code>Rating :</code> " + app_rating.replace(
            "Rated ", "⭐ "
        ).replace(" out of ", "/").replace(" stars", "", 1).replace(
            " stars", "⭐ "
        ).replace(
            "five", "5"
        )
        app_details += (
            "\n<code>Features :</code> <a href='"
            + app_link
            + "'>View in Play Store</a>"
        )
        app_details += "\n\n•••> **Pikabot** <•••"
        await pika_msg(a, app_details, link_preview=True, parse_mode="HTML")
    except IndexError:
        await pika_msg(a, "No result found in search. Please enter **Valid app name**")
    except Exception as err:
        await pika_msg(a, "Exception Occured:- " + str(err))


async def _welcome(_pika):
    _pika_id = await get_pika_id(_pika)
    pika_wel = get_welcome(_pika.chat_id, _pika_id)
    if pika_wel:
        if (_pika.user_joined or _pika.user_added) and not (await _pika.get_user()).bot:
            if pika_wel.cl_wc:
                try:
                    await _pika.client.delete_messages(_pika.chat_id, pika_wel.prev_wc)
                except Exception as e:
                    pikalog.warn(str(e))
            pika1 = await _pika.get_user()
            chat = await _pika.get_chat()
            me = await _pika.client.get_me()

            title = chat.title if chat.title else "this chat"
            participants = await _pika.client.get_participants(chat)
            count = len(participants)
            mention = "[{}](tg://user?id={})".format(pika1.first_name, pika1.id)
            my_mention = "[{}](tg://user?id={})".format(me.first_name, me.id)
            first = pika1.first_name
            last = pika1.last_name
            if last:
                fullname = f"{first} {last}"
            else:
                fullname = first
            username = f"@{pika1.username}" if pika1.username else mention
            userid = pika1.id
            my_first = me.first_name
            my_last = me.last_name
            if my_last:
                my_fullname = f"{my_first} {my_last}"
            else:
                my_fullname = my_first
            my_username = f"@{me.username}" if me.username else my_mention
            file_media = None
            current_saved_welcome_message = None
            if pika_wel and pika_wel.mf_id:
                pikamsg = await _pika.client.get_messages(
                    entity=BOTLOG_CHATID, ids=int(pika_wel.mf_id)
                )
                file_media = pikamsg.media
                current_saved_welcome_message = pikamsg.message
            elif pika_wel and pika_wel.cust_wc:
                current_saved_welcome_message = pika_wel.cust_wc
            current_message = await _pika.reply(
                current_saved_welcome_message.format(
                    mention=mention,
                    title=title,
                    count=count,
                    first=first,
                    last=last,
                    fullname=fullname,
                    username=username,
                    userid=userid,
                    my_first=my_first,
                    my_last=my_last,
                    my_fullname=my_fullname,
                    my_username=my_username,
                    my_mention=my_mention,
                ),
                file=file_media,
            )
            upd_prev_welcome(_pika.chat_id, _pika_id, current_message.id)


async def set_wlcm(_pika):
    _pika_id = await get_pika_id(_pika)
    _tg = await is_pikatg(_pika)
    msg = await _pika.get_reply_message()
    string = _pika.pattern_match.group(1)
    pikaa_id = None
    cln_wc = False
    a = await pika_msg(_pika, "Setting Up Welcome Note, Please Wait...", _tg)
    if msg and msg.media and not string:
        if BOTLOG_CHATID:
            await _pika.client.send_message(
                BOTLOG_CHATID,
                f"#WELCOME_NOTE\
            \nCHAT ID: {_pika.chat_id}\
            \nThe following message is saved as the new welcome note for the chat, please do NOT delete it !!",
            )
            pikamsg = await _pika.client.forward_messages(
                entity=BOTLOG_CHATID, messages=msg, from_peer=_pika.chat_id, silent=True
            )
            pikaa_id = pikamsg.id
        else:
            await pika_msg(
                a,
                "`Saving media as part of the welcome note requires the BOTLOG_CHATID to be set.`",
            )
            return
    elif _pika.reply_to_msg_id and not string:
        rep_msg = await _pika.get_reply_message()
        string = rep_msg.text
    success = "`Welcome note {} for this chat.`"
    if add_welcome(
            _pika.chat_id,
            _pika_id,
            string,
            cln_wc,
            0,
            pikaa_id) is True:
        await pika_msg(a, success.format("saved"))
    else:
        await pika_msg(a, success.format("updated"))


async def get_welcm(_pika):
    _pika_id = await get_pika_id(_pika)
    pika_wel = get_welcome(_pika.chat_id, _pika_id)
    _tg = await is_pikatg(_pika)
    a = await pika_msg(_pika, "Getting Current Welcome Message, Please Wait...", _tg)
    if not pika_wel:
        await pika_msg(a, "`No welcome message saved here.`")
        return
    elif pika_wel and pika_wel.mf_id:
        pikamsg = await _pika.client.get_messages(
            entity=BOTLOG_CHATID, ids=int(pika_wel.mf_id)
        )
        await pika_msg(
            a, "`I am currently welcoming new users with this welcome note.`"
        )
        await _pika.reply(pikamsg.message, file=pikamsg.media)
    elif pika_wel and pika_wel.cust_wc:
        await pika_msg(
            a, "`I am currently welcoming new users with this welcome note.`"
        )
        await _pika.reply(pika_wel.cust_wc)


async def del_welcm(_pika):
    _tg = await is_pikatg(_pika)
    _pika_id = await get_pika_id(_pika)
    a = await pika_msg(_pika, "Deleting Welcome Note, Please wait...", _tg)
    if remove_welcome(_pika.chat_id, _pika_id) is True:
        await pika_msg(a, "`Welcome note deleted for this chat.`")
    else:
        await pika_msg(a, "`Do I have a welcome note here ?`")


async def clean_welcm(_pika):
    _tg = await is_pikatg(_pika)
    _pika_id = await get_pika_id(_pika)
    a = await pika_msg(
        _pika, "Turning On Welcome Note Auto cleaning AI, Please wait...", _tg
    )
    clean_welcome(_pika.chat_id, _pika_id, True)
    await pika_msg(a, "**Sucessfully Turned on Welcome Note Auto cleaning**")


async def _telegraph(event):
    telegraph = Telegraph()
    r = telegraph.create_account(short_name=Config.TELEGRAPH_SHORT_NAME)
    auth_url = r["auth_url"]
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    await event.client.send_message(
        Config.PLUGIN_CHANNEL,
        "Created New Telegraph account {} for the current session. \n**Do not give this url to anyone, even if they say they are from Telegram!**".format(
            auth_url
        ),
    )
    _tg = await get_pika_tg(event)
    a = await pika_msg(event, "Generating Telegraph Link, Please wait...", _tg)
    optional_title = event.pattern_match.group(2)
    if event.reply_to_msg_id:
        start = pikatime.now()
        r_message = await event.get_reply_message()
        input_str = event.pattern_match.group(1)
        await get_pika_tg(event)
        if input_str == "m":
            downloaded_file_name = await event.client.download_media(
                r_message, Config.TMP_DOWNLOAD_DIRECTORY
            )
            end = pikatime.now()
            ms = (end - start).seconds
            if downloaded_file_name.endswith((".webp")):
                resize_image(downloaded_file_name)
            try:
                start = pikatime.now()
                media_urls = upload_file(downloaded_file_name)
            except exceptions.TelegraphException as exc:
                await pika_msg(a, "ERROR: " + str(exc))
                os.remove(downloaded_file_name)
            else:
                end = pikatime.now()
                ms_two = (end - start).seconds
                os.remove(downloaded_file_name)
                await pika_msg(
                    a,
                    "𝐓𝐞𝐥𝐞𝐠𝐫𝐚𝐩𝐡.𝐩𝐡 𝐋𝐢𝐧𝐤 👉 `https://telegra.ph{}`".format(
                        media_urls[0], (ms + ms_two)
                    ),
                    link_preview=false,
                )
        elif input_str == "t":
            user_object = await event.client.get_entity(r_message.sender_id)
            title_of_page = user_object.first_name  # + " " + user_object.last_name
            # apparently, all Users do not have last_name field
            if optional_title:
                title_of_page = optional_title
            page_content = r_message.message
            if r_message.media:
                if page_content != "":
                    title_of_page = page_content
                downloaded_file_name = await event.client.download_media(
                    r_message, Config.TMP_DOWNLOAD_DIRECTORY
                )
                m_list = None
                with open(downloaded_file_name, "rb") as fd:
                    m_list = fd.readlines()
                for m in m_list:
                    page_content += m.decode("UTF-8") + "\n"
                os.remove(downloaded_file_name)
            page_content = page_content.replace("\n", "<br>")
            response = telegraph.create_page(
                title_of_page, html_content=page_content)
            end = pikatime.now()
            ms = (end - start).seconds
            await pika_msg(
                a,
                "𝐓𝐞𝐥𝐞𝐠𝐫𝐚𝐩𝐡.𝐩𝐡 𝐋𝐢𝐧𝐤 👉 `https://telegra.ph{}`".format(response["path"]),
                link_preview=True,
            )
    else:
        await pika_msg(a, "Reply to a msg/media to get a permanent telegra.ph link.")


def resize_image(image):
    im = Image.open(image)
    im.save(image, "PNG")


async def _invite(event):
    if event.fwd_from:
        return
    to_add_users = event.pattern_match.group(1)
    if event.is_private:
        await event.edit("`.invite` users to a chat, not to a Private Message")
    else:
        pikalog.info(to_add_users)
        if not event.is_channel and event.is_group:
            # https://lonamiwebs.github.io/Telethon/methods/messages/add_chat_user.html
            for user_id in to_add_users.split(" "):
                try:
                    await event.client(
                        functions.messages.AddChatUserRequest(
                            chat_id=event.chat_id, user_id=user_id, fwd_limit=1000000
                        )
                    )
                except Exception as e:
                    await event.reply(str(e))
            await event.edit("Invited Successfully ji")
        else:
            # https://lonamiwebs.github.io/Telethon/methods/channels/invite_to_channel.html
            for user_id in to_add_users.split(" "):
                try:
                    await event.client(
                        functions.channels.InviteToChannelRequest(
                            channel=event.chat_id, users=[user_id]
                        )
                    )
                except Exception as e:
                    await event.reply(str(e))
            await event.edit("Invited Successfully")


async def _ping(event):
    if event.fwd_from:
        return
    if await is_pikatg(event):
        az = f"{bot.me.first_name}'s **Assistant**"
    else:
        axx = await pikaa(event, "ALIVE_NAME")
        az = f"𝑴𝒚 𝑩𝒐𝒔𝒔 **{axx}**"
    _tg = await get_pika_tg(event)
    start = pikatime.now()
    a = await pika_msg(event, f"{rx}pikaa", _tg)
    end = pikatime.now()
    ms = (end - start).microseconds / 1000
    await pika_msg(a, "✪ 𝗣𝗂𝗄𝖺 𝗣𝗂𝗄𝖺 𝗣𝗂𝗄𝖺𝖼𝗁𝗎!\n➥{}Ms\n➥{}".format(ms, az))
    await asyncio.sleep(7)
    await a.delete()
