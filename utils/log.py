# _*_ coding:utf-8 _*_
# Copyright (C) 2024-2024 shiyi0x7f,Inc.All Rights Reserved
# @Time : 2024/6/9 上午10:01
# @Author: shiyi0x7f
from .config import config_manager
from loguru import logger
import os
def only_logger():
    return logger
log = only_logger()
BASE_DIR = config_manager.get('base_dir')
log_path = os.path.join(BASE_DIR,'logs')
if not os.path.isdir(log_path):
    os.mkdir(log_path)
log.add(os.path.join(log_path,"warning.log"),level="WARNING",rotation="10 MB")  # 当文件达到10MB时自动切割
log.add(os.path.join(log_path,"error.log"),level="ERROR",rotation="10 MB")  # 当文件达到10MB时自动切割
if __name__ == '__main__':
    print(log_path)