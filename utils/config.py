# _*_ coding:utf-8 _*_
# Copyright (C) 2024-2024 shiyi0x7f,Inc.All Rights Reserved
# @Time : 2024/6/3 下午10:46
# @Author: shiyi0x7f
from configparser import ConfigParser
import os

class ConfigManager:
    def __init__(self, filename):
        self.filename = filename
        self.config = ConfigParser()
        if not os.path.exists(filename):
            self.config_init()
        self.config.read(self.filename)

    def config_init(self):
        defaults = {
            'BASE_API_URL': "https://api.11xy.cn",
            'BASE_URL': 'https://singlelogin.re',
            'BASE_HOST': 'singlelogin.re',
            'remix_key': '',
            'remix_id': '',
            'save_path': os.path.join(
                os.path.expanduser('~'), 'Downloads')
        }
        for key, value in defaults.items():
            self.set(key, value)
        self.save()
        print("初始化成功")

    def get(self, option,section='default'):
        return self.config.get(section, option)

    def set(self, option=None,value=None,section='default'):
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, option, value)

    def save(self):
        with open(self.filename, 'w') as configfile:
            self.config.write(configfile)

    def remove_option(self, option, section='default'):
        if self.config.has_section(section):
            self.config.remove_option(section, option)

    def remove_section(self, section='default'):
        self.config.remove_section(section)

    def has_option(self,option, section='default'):
        return self.config.has_option(section, option)

    def has_section(self, section='default'):
        return self.config.has_section(section)

EXEMODE = 1 #0 源代码模式   1打包运行模式

BASE_DIR = os.getcwd() if EXEMODE else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 创建全局的 config_manager 实例
config_manager = ConfigManager(os.path.join(BASE_DIR,'config.ini'))
if not config_manager.has_option('BASE_DIR'):
    config_manager.set('BASE_DIR',BASE_DIR)
    config_manager.save()

if __name__ == '__main__':
    # 使用示例
    try:
        s = config_manager.get('base_host')
        print(s)
    except Exception as e:
        print(e)
    # 保存配置
    #config_manager.save()

