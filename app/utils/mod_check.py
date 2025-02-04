# _*_ coding:utf-8 _*_
# Copyright (C) 2024-2024 shiyi0x7f,Inc.All Rights Reserved
# @Time : 2024/12/20 下午8:33
# @Author: shiyi0x7f
import requests
import webbrowser
from loguru import logger
from .mod_domain import get_domain
from ..common.config import cfg,VERSION
from qfluentwidgets import Dialog

class CheckUpdate():
    def __init__(self):
        self.__config = None
        self.__get_config()
    def __get_config(self):
        domain = get_domain()
        api_config = f'{domain}/OlibServer'
        resp = requests.get(api_config)
        print(api_config)
        self.__config = resp.json()

    def __get_version_status(self):
        if self.__config is None:
            self.__get_config()
        client_ver = VERSION
        server_vers = self.__config.get('Versions')
        latest = server_vers[-1]
        versions = []
        for ver in server_vers:
            versions.append(ver.get('version'))
        latest_ver = versions[-1]
        cfg.set(cfg.latestVersion,latest_ver)
        forced = latest.get('forcedUpdate')
        if latest_ver != client_ver and client_ver in versions:#保证在已有版本内
            logger.warning(f"当前版本不是最新版本 客户端{client_ver} 服务端{latest_ver}")
            if forced:
                return 2 #强制更新
            else:
                return 1 #可跳过更新
        return 0 #最新版本无操作

    def get_notice(self):
        if self.__config is None:
            self.__get_config()
        server_notice = self.__config.get('Notice')
        return server_notice

    def get_update_url(self):
        if self.__config is None:
            self.__get_config()
        update_url = self.__config.get('UpdateUrl')
        return update_url

    def handle_version(self):
        n = self.__get_version_status()
        if n==1:
            update_window = Dialog("更新选项","新版本功能更加丰富稳定哦~")
            update_window.yesButton.setText("立即更新")
            update_window.cancelButton.setText("下次再说")
            if update_window.exec_():
                self.update_()
                exit(0)
            else:
                cfg.set(cfg.updateMode,False)
        elif n==2:
            forcedUpdateWin = Dialog("强制更新","是否进入更新界面")
            if forcedUpdateWin.exec_():
                logger.info("开始强制更新")
                self.update_()
            else:
                logger.warning("取消强制更新")
            exit(0)
    def update_(self):
        update_url = self.get_update_url()
        webbrowser.open(update_url)

