# _*_ coding:utf-8 _*_
# Copyright (C) 2024-2024 shiyi0x7f,Inc.All Rights Reserved
# @Time : 2024/12/20 下午9:21
# @Author: shiyi0x7f
from .mod_env import get_env
from ..common.config import TESTHOST,PRODHOST,DEVHOST

def get_domain():
    env = get_env()
    if env=='dev':
        url = f'http://{DEVHOST}'
    elif env=='test':
        url = f'https://{TESTHOST}'
    else:
        url = f'https://{PRODHOST}'
    return url