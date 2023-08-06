from ..database import *


class pdb(object):
    api_id = _get("API_ID")
    api_hash = _get("API_HASH")
    bf_token = _get("TG_BOT_TOKEN_BF_HER")
    bf_uname = _get("TG_BOT_USER_NAME_BF_HER")
    maincl = pget("main", "session")
    multicl1 = pget("multi1", "session")
    multicl2 = pget("multi2", "session")
    multicl3 = pget("multi3", "session")
