# _*_ coding:utf-8 _*_
# Copyright (C) 2023-2023 shiyi0x7f,Inc.All Rights Reserved
# @Time : 2023/6/7 22:42
# @Author: shiyi0x7f

from PyQt5.QtWidgets import QMessageBox,QDialog
from PyQt5.QtCore import pyqtSignal
from .config_window_ui import Ui_Dialog
from OpenLib.utils.config import config_manager
from OpenLib.utils.log import log
import webbrowser


#配置子窗口
class ConfigChildWindow(QDialog,Ui_Dialog):
    user_data = pyqtSignal(object)
    sig_downnum = pyqtSignal(int)
    def __init__(self):
        super(ConfigChildWindow, self).__init__()
        self.setupUi(self)
        self.howBtn.clicked.connect(self.get_key_id)
        self.configBtn.clicked.connect(self.setting_config)
        txtChange = lambda: self.configBtn.setEnabled(self.actEdit.text() != '' and self.pwdEdit.text() != '')
        txtChange()
        self.actEdit.textChanged.connect(txtChange)
        self.pwdEdit.textChanged.connect(txtChange)


        try:
            key_ = config_manager.get("remix_key")
            id_ = config_manager.get("remix_id")
            self.actEdit.setText(key_)
            self.pwdEdit.setText(id_)
        except KeyError:
            pass

    def get_key_id(self):
        url = "https://www.baidu.com"
        webbrowser.open(url)

    # 设置配置文件
    def setting_config(self):
        key_ = config_manager.get("remix_key")
        id_ = config_manager.get("remix_id")
        if self.actEdit.text() != key_:
            config_manager.set("remix_key", key_)
        if self.pwdEdit.text() != id_:
            config_manager.set("remix_id", id_)
        config_manager.save()
        log.success("配置设置成功")
        self.close()

if __name__ == '__main__':
    pass