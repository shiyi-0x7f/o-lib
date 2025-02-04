# _*_ coding:utf-8 _*_
# Copyright (C) 2024-2024 shiyi0x7f,Inc.All Rights Reserved
# @Time : 2024/12/6 上午8:16
# @Author: shiyi0x7f
import time
import requests
from loguru import logger as log
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (QVBoxLayout, QFrame,
                             QHeaderView, QTableWidgetItem,
                             QProgressBar)
from qfluentwidgets import TableWidget,BodyLabel
from ..tools.olib_download import OlibDownloaderV4


class DownloadInterface(QFrame):
    finished = pyqtSignal(bool,str)
    sig_start = pyqtSignal(str)
    sig_rate_limit = pyqtSignal(bool)
    def __init__(self,obj_name):
        super().__init__()
        self.setObjectName(obj_name)
        self.rowCount = 0
        # 初始化布局
        self.layout = QVBoxLayout(self)
        self.initUI()


    def initUI(self):
        #初始化展示页
        self.tableWidget = TableWidget(self)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setEditTriggers(TableWidget.NoEditTriggers)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setHorizontalHeaderLabels(["书名","进度","速度"])

        # #添加组件
        self.layout.addWidget(self.tableWidget)

    def add_download_item(self,title,process,operate):

        '''
        :param title:str
        :param process:QProcess
        :param operate:PushButton
        :return:
        '''
        self.tableWidget.insertRow(
            self.tableWidget.rowCount())  # 添加
        item_title = QTableWidgetItem(title)
        self.tableWidget.setItem(self.rowCount, 0, item_title)
        self.tableWidget.setCellWidget(self.rowCount, 1, process)
        self.tableWidget.setCellWidget(self.rowCount, 2, operate)
        self.rowCount += 1 #更新行号

    def download(self,bookid,hashid,bookname,extension,size):
        downloader = OlibDownloaderV4(bookid, hashid,bookname, extension,size)
        progressBar = QProgressBar()
        progressBar.setRange(0, 100)
        progressBar.setAlignment(Qt.AlignCenter)

        speedLabel = BodyLabel()
        speedLabel.setAlignment(Qt.AlignCenter)

        # 连接独立的槽方法
        downloader.sig_down_process.connect(
            lambda value, pb=progressBar: pb.setValue(
                value))
        downloader.speed.connect(
            lambda speed, lbl=speedLabel: lbl.setText(
                f"{speed} KB/s"))
        downloader.final.connect(lambda e, bn=bookname: self.finish(e, bn))
        downloader.finished.connect(lambda: downloader.deleteLater())
        downloader.sig_start.connect(lambda :self.download_start(bookname,progressBar,speedLabel))
        downloader.sig_rate_limit.connect(self.sent_rate_limit)
        downloader.start()
    def download_start(self,bookname, progressBar,speedLabel):
        self.add_download_item(bookname, progressBar,speedLabel)
        log.info("下载页面接收到开始")
        self.sig_start.emit(bookname)

    def sent_rate_limit(self,e):
        self.sig_rate_limit.emit(True)

    def finish(self,e,bookname):
        self.finished.emit(e,bookname)

