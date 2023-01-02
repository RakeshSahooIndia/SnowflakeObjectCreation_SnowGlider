import base64

import snowflake.connector
from configparser import ConfigParser
from config import get_secrets


# connect to snow flake database using credentials saved in config.ini file

def snowflake_acct_connect(acct_option):
    try:
        encode_sec = base64.b64encode(str(acct_option).encode("ascii"))
        snwflk_usr = get_secrets(encode_sec, "user")
        snwflk_pwd = get_secrets(encode_sec, "password")
        con = snowflake.connector.connect(
            user=snwflk_usr,
            password=snwflk_pwd,
            account=acct_option
        )
        return con
    except Exception as e:
        return None


def snowflake_ws_connect(acct_option):
    encode_sec = base64.b64encode(str(acct_option).encode("ascii"))
    snwflk_usr = get_secrets(encode_sec, "user")
    snwflk_pwd = get_secrets(encode_sec, "password")
    snwflk_ws = get_secrets(encode_sec, "warehouse")
    try:
        con = snowflake.connector.connect(
            user=snwflk_usr,
            password=snwflk_pwd,
            account=acct_option,
            warehouse=snwflk_ws
        )
        return con
    except Exception as e:
        return None
