import base64
from configparser import ConfigParser

# read config.ini

def get_ini_sections():
    configur = ConfigParser()
    configur.read('config.ini')
    sec_list = ['<select account>']
    for each_section in configur.sections():
        b64decode_byte = base64.b64decode(each_section)
        sec_list.append(b64decode_byte.decode("ascii"))

    return sec_list


def get_secrets(section, key):
    configur = ConfigParser()
    configur.read('config.ini')
    b64decode_byte2 = base64.b64decode(configur.get(section.decode("ascii"), key))
    return b64decode_byte2.decode("ascii")