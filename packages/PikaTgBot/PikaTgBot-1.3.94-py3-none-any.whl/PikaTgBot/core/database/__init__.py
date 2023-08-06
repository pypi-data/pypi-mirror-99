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

from urllib.parse import urlparse
from sqlalchemy import *
from rejson import Client, Path
import os

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
_get = os.environ.get

# the secret configuration specific things


def start() -> scoped_session:
    engine = create_engine(_get("DATABASE_URL"))
    BASE.metadata.bind = engine
    BASE.metadata.create_all(engine)
    return scoped_session(sessionmaker(bind=engine, autoflush=False))


try:
    BASE = declarative_base()
    SESSION = start()
except AttributeError as e:
    # this is a dirty way for the work-around required for #23
    print("DB_URI is not configured. Features depending on the database might have issues.")
    print(str(e))


class BotUsers(BASE):
    __tablename__ = "botusers"
    pika_id = Column(String(14), primary_key=True)

    def __init__(self, pika_id):
        self.pika_id = pika_id


class PikaChats(BASE):
    __tablename__ = "PikaTg"
    pika_id = Column(String(14), primary_key=True)

    def __init__(self, pika_id):
        self.pika_id = pika_id


class GMute(BASE):
    __tablename__ = "gmute"
    sender = Column(String(14), primary_key=True)
    pika_id = Column(Numeric, primary_key=True)

    def __init__(self, sender, pika_id):
        self.sender = str(sender)
        self.pika_id = pika_id


class GBan(BASE):
    __tablename__ = "gban"
    sender = Column(String(14), primary_key=True)
    pika_id = Column(Numeric, primary_key=True)
    reason = Column(UnicodeText)

    def __init__(self, sender, pika_id, reason=""):
        self.sender = str(sender)
        self.pika_id = str(pika_id)
        self.reason = reason


class Mute(BASE):
    __tablename__ = "mute"
    sender = Column(String(14), primary_key=True)
    chat_id = Column(String(14), primary_key=True)
    pika_id = Column(Numeric, primary_key=True)

    def __init__(self, sender, chat_id, pika_id):
        self.sender = str(sender)
        self.chat_id = str(chat_id)
        self.pika_id = pika_id


class Notes(BASE):
    __tablename__ = "notes"
    chat_id = Column(String(14), primary_key=True)
    keyword = Column(UnicodeText, primary_key=True, nullable=False)
    reply = Column(UnicodeText)
    f_mesg_id = Column(Numeric)
    client_id = Column(Numeric, primary_key=True)

    def __init__(self, chat_id, keyword, reply, f_mesg_id, client_id):
        self.chat_id = str(chat_id)
        self.keyword = keyword
        self.reply = reply
        self.f_mesg_id = f_mesg_id
        self.client_id = client_id


class PMPermit(BASE):
    __tablename__ = "pmpermit"
    chat_id = Column(String(14), primary_key=True)
    reason = Column(String(127))
    pika_id = Column(Numeric, primary_key=True)

    def __init__(self, chat_id, pika_id, reason=""):
        self.chat_id = chat_id
        self.reason = reason
        self.pika_id = pika_id


class Welcome(BASE):
    __tablename__ = "welcome"
    chat_id = Column(String(14), primary_key=True)
    pika_id = Column(Numeric, primary_key=True)
    cust_wc = Column(UnicodeText)
    cl_wc = Column(Boolean, default=False)
    prev_wc = Column(BigInteger)
    mf_id = Column(UnicodeText)

    def __init__(self, chat_id, pika_id, cust_wc, cl_wc, prev_wc, mf_id=None):
        self.chat_id = chat_id
        self.pika_id = pika_id
        self.cust_wc = cust_wc
        self.cl_wc = cl_wc
        self.prev_wc = prev_wc
        self.mf_id = mf_id


Mute.__table__.create(checkfirst=True)
BotUsers.__table__.create(checkfirst=True)
PikaChats.__table__.create(checkfirst=True)
GMute.__table__.create(checkfirst=True)
GBan.__table__.create(checkfirst=True)
Notes.__table__.create(checkfirst=True)
PMPermit.__table__.create(checkfirst=True)
Welcome.__table__.create(checkfirst=True)


def add_welcome(chat_id, pika_id, cust_wc, cl_wc, prev_wc, mf_id):
    add_wc = Welcome(chat_id, pika_id, cust_wc, cl_wc, prev_wc, mf_id)
    SESSION.add(add_wc)
    SESSION.commit()


def remove_welcome(chat_id, pika_id):
    rm_wc = SESSION.query(Welcome).get((str(chat_id), pika_id))
    if rm_wc:
        SESSION.delete(rm_wc)
        SESSION.commit()


def upd_prev_welcome(chat_id, pika_id, prev_wc):
    _update = SESSION.query(Welcome).get((str(chat_id), pika_id))
    _update.prev_wc = prev_wc
    SESSION.commit()


def get_welcome(chat_id, pika_id):
    try:
        return SESSION.query(Welcome).get((str(chat_id), pika_id))
    except Exception as e:
        pikalog.error(str(e))
        return
    finally:
        SESSION.close()


def clean_welcome(chat_id, pika_id, cl_wc):
    clnn = SESSION.query(Welcome).get((str(chat_id), pika_id))
    clnn.cl_wc = cl_wc
    SESSION.commit()


def approve(chat_id, pika_id, reason):
    adder = PMPermit(str(chat_id), pika_id, str(reason))
    SESSION.add(adder)
    SESSION.commit()


def disapprove(chat_id, pika_id):
    rem = SESSION.query(PMPermit).get((str(chat_id), pika_id))
    if rem:
        SESSION.delete(rem)
        SESSION.commit()


def get_all_approved(pika_id):
    rem = SESSION.query(PMPermit).filter(PMPermit.pika_id == pika_id).all()
    SESSION.close()
    return rem


def is_approved(chat_id, pika_id):
    try:
        return SESSION.query(PMPermit).filter(
            PMPermit.chat_id == str(chat_id),
            PMPermit.pika_id == pika_id).one()
    except BaseException:
        return None
    finally:
        SESSION.close()


def get_note(chat_id, keyword, client_id):
    try:
        return SESSION.query(Notes).get((str(chat_id), keyword, client_id))
    finally:
        SESSION.close()


def get_notes(chat_id, client_id):
    try:
        return SESSION.query(Notes).filter(
            Notes.chat_id == str(chat_id),
            Notes.client_id == client_id).all()
    except BaseException:
        return None
    finally:
        SESSION.close()


def add_note(chat_id, keyword, reply, f_mesg_id, client_id):
    to_check = get_note(chat_id, keyword, client_id)
    if not to_check:
        adder = Notes(str(chat_id), keyword, reply, f_mesg_id, client_id)
        SESSION.add(adder)
        SESSION.commit()
        return True
    else:
        rem = SESSION.query(Notes).get((str(chat_id), keyword, client_id))
        SESSION.delete(rem)
        SESSION.commit()
        adder = Notes(str(chat_id), keyword, reply, f_mesg_id, client_id)
        SESSION.add(adder)
        SESSION.commit()
        return False


def rm_note(chat_id, keyword, client_id):
    to_check = get_note(chat_id, keyword, client_id)
    if not to_check:
        return False
    else:
        rem = SESSION.query(Notes).get((str(chat_id), keyword, client_id))
        SESSION.delete(rem)
        SESSION.commit()
        return True


def is_muted(sender, chat_id, pika_id):
    user = SESSION.query(Mute).get((str(sender), str(chat_id), pika_id))
    if user:
        return True
    else:
        return False


def mute(sender, chat_id, pika_id):
    adder = Mute(str(sender), str(chat_id), pika_id)
    SESSION.add(adder)
    SESSION.commit()


def unmute(sender, chat_id, pika_id):
    rem = SESSION.query(Mute).get((str(sender), str(chat_id), pika_id))
    if rem:
        SESSION.delete(rem)
        SESSION.commit()


def get_all_muted(pika_id):
    rem = SESSION.query(Mute).filter(Notes.pika_id == pika_id).all()
    SESSION.close()
    return rem


def is_gbanned(sender, pika_id):
    try:
        _pikaG = SESSION.query(GBan).get((str(sender), str(pika_id)))
        if _pikaG:
            return str(_pikaG.reason)
    finally:
        SESSION.close()


def gban(sender, pika_id, reason):
    adder = GBan(str(sender), str(pika_id), str(reason))
    SESSION.add(adder)
    SESSION.commit()


def ungban(sender, pika_id):
    rem = SESSION.query(GBan).get((str(sender), str(pika_id)))
    if rem:
        SESSION.delete(rem)
        SESSION.commit()


def is_gmuted(sender):
    try:
        return SESSION.query(GMute).all()
    except BaseException:
        return None
    finally:
        SESSION.close()


def gmute(sender, pika_id):
    adder = GMute(str(sender), pika_id)
    SESSION.add(adder)
    SESSION.commit()


def ungmute(sender, pika_id):
    rem = SESSION.query(GMute).get((str(sender), pika_id))
    if rem:
        SESSION.delete(rem)
        SESSION.commit()


def add_pika(pika_id):
    pika = PikaChats(str(pika_id))
    SESSION.add(pika)
    SESSION.commit()


def is_pika_exist(pika_id):
    try:
        pika = SESSION.query(PikaChats).filter(
            PikaChats.pika_id == str(pika_id)).one()
        if pika:
            return True
    except BaseException:
        return None
    finally:
        SESSION.close()


def get_pika_chats():
    try:
        pika = SESSION.query(PikaChats).all()
        if pika:
            return pika
    except BaseException:
        return None
    finally:
        SESSION.close()


def add_user(pika_id: int):
    pika = BotUsers(str(pika_id))
    SESSION.add(pika)
    SESSION.commit()


def is_user_exist(pika_id):
    try:
        pika = SESSION.query(BotUsers).filter(
            BotUsers.pika_id == str(pika_id)).one()
        if pika:
            return True
    except BaseException:
        return None
    finally:
        SESSION.close()


def get_added_users():
    pika = SESSION.query(BotUsers).all()
    SESSION.close()
    return pika


uri = _get("REDIS_ENDPOINT").split(":")
host = uri[0]
port = uri[1]
password = _get("REDIS_PASSWORD")
pikadb = Client(
    host=host,
    port=port,
    password=password,
    decode_responses=True)
pikaset = pikadb.jsonset
pikadel = pikadb.jsondel
pikaget = pikadb.jsonget

cdata = {
    'main': {
        'session': None,
        'pmsecurity': False,
        'pmmsg': None,
        'alivename': None,
        'alivepic': None,
        'alivemsg': None,
        'userbio': None,
        'cmdhandler': None,
        'pmlogger': None,
        'botlog': None,
        'auser': None,
        'dauser': None
    },
    'multi1': {
        'session': None,
        'pmsecurity': False,
        'pmmsg': None,
        'alivename': None,
        'alivepic': None,
        'alivemsg': None,
        'userbio': None,
        'pmlogger': None,
        'auser': None,
        'dauser': None
    },
    'multi2': {
        'session': None,
        'pmsecurity': False,
        'pmmsg': None,
        'alivename': None,
        'alivepic': None,
        'alivemsg': None,
        'userbio': None,
        'pmlogger': None,
        'auser': None
    },
    'multi3': {
        'session': None,
        'pmsecurity': False,
        'pmmsg': None,
        'alivename': None,
        'alivepic': None,
        'alivemsg': None,
        'userbio': None,
        'pmlogger': None,
        'auser': None,
        'dauser': None
    },
    'apis': {
        'youtubeapi': None,
        'lyndiaapi': None,
        'screenshotapi': None,
        'removebgapi': None
    },
}


def startdb():
    old_db_exists = pikaget('cdata', Path.rootPath())
    if not old_db_exists:
        pikaset("cdata", Path.rootPath(), cdata)
    else:
        return


startdb()


def pset(rejsclt, data, value):
    return pikaset('cdata', Path(f".{rejsclt.data}"), value)


def pget(rejsclt, data):
    return pikaget('cdata', Path(f".{rejsclt.data}"))


def pdel(rejsclt, value):
    return pikadel('cdata', Path(f".{rejsclt.data}"))


class pdb(object):
    api_id = _get("API_ID")
    api_hash = _get("API_HASH")
    bf_token = _get("TG_BOT_TOKEN_BF_HER")
    bf_uname = _get("TG_BOT_USER_NAME_BF_HER")
    maincl = pget("main", "session")
    multicl1 = pget("multi1", "session")
    multicl2 = pget("multi2", "session")
    multicl3 = pget("multi3", "session")
