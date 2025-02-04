# _*_ coding:utf-8 _*_
# Copyright (C) 2024-2024 shiyi0x7f,Inc.All Rights Reserved
# @Time : 2024/12/4 下午9:52
# @Author: shiyi0x7f
from dotenv import load_dotenv
import os
def get_env():
    load_dotenv()
    env = os.getenv('APP_ENV')
    if env:
        return env.lower()
    return "prod"
if __name__ == '__main__':
    env = get_env()
    print(env)