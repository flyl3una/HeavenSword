#! env/bin/python
# coding:utf-8

import os
from HeavenSword.settings import BASE_DIR

CORE_PATH = os.path.join(BASE_DIR, 'core')

DICT_PATH = os.path.join(CORE_PATH, 'setting', 'dict')
EXP_PATH = os.path.join(CORE_PATH, 'setting', 'exp')
FINGER_PATH = os.path.join(CORE_PATH, 'setting', 'finger')

INTERNET_TIMEOUT = 0.3


DB_HOST = "127.0.0.1"
DB_USER = "root"
DB_PASSWORD = ""
DB_PORT = 3306
DB_NAME = "heavensword"
DB_CHARSET = "utf8"
