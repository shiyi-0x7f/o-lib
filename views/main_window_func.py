# _*_ coding:utf-8 _*_
# Copyright (C) 2023-2023 shiyi0x7f,Inc.All Rights Reserved
# @Time : 2023/6/7 20:22
# @Author: shiyi0x7f
# 参数模块
# UI模块
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QAbstractItemView
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMenu
from PyQt5.QtWidgets import QProgressBar
from PyQt5.QtWidgets import QHeaderView
from PyQt5.QtCore import Qt
from .config_window_func import ConfigChildWindow
from .main_window_ui import Ui_MainWindow
# 功能模块
from OpenLib.controllers.zlibsearch import ZlibSearcherV3
from OpenLib.controllers.zlibdownload import ZlibDownloader3
from OpenLib.utils.config import config_manager
from OpenLib.utils.log import log

import qtawesome as qta
import re
import os
import sys
import random
import webbrowser

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        # 固定用法
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        # 初始化参数
        self.page = 0
        self.m_dctThread2Download = {}  # 下载线程

        # 按钮绑定槽函数
        self.statusBar().showMessage('无动作')
        self.queryBtn.clicked.connect(self.query)
        self.bookEdit.returnPressed.connect(self.query)
        # 菜单绑定槽函数
        self.exitBtn.triggered.connect(self.close)
        self.configAction.triggered.connect(self.setting)
        self.aboutAction.triggered.connect(self.about_developer)
        self.websiteAction.triggered.connect(self.find_me)

        self.preBtn.clicked.connect(self.pre_page)
        self.nextBtn.clicked.connect(self.next_page)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        # 表格初始化
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setHorizontalHeaderLabels(["书名", "作者", "年份", "格式", "大小"])
        self.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tableWidget.customContextMenuRequested.connect(self.generateMenu)
        self.tableWidget.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        # 书籍格式 combobox初始化
        self.brBox.addItems(['所有', 'AZW', 'AZW3', 'EPUB', 'MOBI', 'PDF', 'TXT'])
        self.brBox.setCurrentIndex(0)
        self.modeBox.addItems(['默认', '热度', '名称', '匹配度', '上传日期', '出版日期'])
        idChange = lambda: self.queryBtn.setEnabled(self.bookEdit.text() != '')
        self.bookEdit.textChanged.connect(idChange)
        idChange()

        self.exitBtn.setIcon(qta.icon('mdi.exit-to-app', scale_factor=1.25))
        self.configAction.setIcon(qta.icon('fa.gear', scale_factor=1.25))
        self.aboutAction.setIcon(qta.icon('fa.info-circle', scale_factor=1.25))
        self.websiteAction.setIcon(qta.icon('mdi.web', scale_factor=1.25))
        self.updateAction.setIcon(qta.icon('mdi.update', scale_factor=1.25))

        self.groupBox.setVisible(False)
        self.proBtn.clicked.connect(self.displayPro)
        self.proBtn.setIcon(qta.icon('fa.chevron-down'))


        path = config_manager.get('save_path')
        self.pathLB.setText(path)
        self.pathBtn.clicked.connect(self.changePath)
        if not config_manager.get('remix_key'):
            QMessageBox.warning(self,"缺少配置","当前缺少关键配置参数，请进行配置。")
            self.setting()

    def displayPro(self):
        if self.groupBox.isVisible():
            self.groupBox.setVisible(False)
            self.resize(self.width(), self.height() - self.groupBox.height() + 2)
            self.proBtn.setIcon(qta.icon('fa.chevron-down'))
        else:
            self.resize(self.width(), self.height() + self.groupBox.height() - 2)
            self.groupBox.setVisible(True)
            self.proBtn.setIcon(qta.icon('fa.chevron-up'))

    def clickDownload(self, downid, bookname, extension):
        save_path = config_manager.get('save_path')
        self.statusBar().showMessage(f"{bookname}开始下载")
        self.reset_downlist_size()
        fileList = os.listdir(save_path)
        filename = f"{bookname}.{extension}"
        if self.skipCheck.isChecked() and filename in fileList:
            self.statusBar().showMessage(f'跳过{filename}，已存在。')
            return
        iRow = self.tableWidgetDownload.rowCount()
        oThreadDownload = ZlibDownloader3(downid,bookname=bookname, extension=extension)
        self.m_dctThread2Download[iRow] = oThreadDownload

        self.tableWidgetDownload.setRowCount(iRow + 1)
        pItem = QTableWidgetItem(bookname)
        self.tableWidgetDownload.setItem(iRow, 0, pItem)
        pItem = QProgressBar()
        pItem.setValue(0)
        self.tableWidgetDownload.setCellWidget(iRow, 1, pItem)
        pItem = QTableWidgetItem("0KB/s")
        self.tableWidgetDownload.setItem(iRow, 2, pItem)

        oThreadDownload.sig_down_process.connect(self.onUpdateProgress)
        oThreadDownload.speed.connect(self.updateSpeed)
        oThreadDownload.final.connect(self.downFinal)

        oThreadDownload.start()


    def downFinal(self, sig):
        if sig is True:
            QMessageBox.warning(self, "下载完毕", "书籍已下载完毕，请尽情阅读")

    # 进度更新
    def onUpdateProgress(self, oThread, iProgress):
        for iRow, oThreadDownload in self.m_dctThread2Download.items():
            if oThread == oThreadDownload:
                self.tableWidgetDownload.cellWidget(iRow, 1).setValue(iProgress)

    def updateSpeed(self, oThread, speed_):
        for iRow, oThreadDownload in self.m_dctThread2Download.items():
            if oThread == oThreadDownload:
                pItem = QTableWidgetItem(f"{speed_}KB/s")
                self.tableWidgetDownload.setItem(iRow, 2, pItem)

    def about_developer(self):
        webbrowser.open("https://space.bilibili.com/19276680")

    # 用户名鼠标进入事件
    def UserEnter(self, e):
        font = self.userLB.font()
        font.setUnderline(True)
        self.userLB.setFont(font)
        return super().enterEvent(e)

    # 用户名鼠标离开事件
    def UserLeave(self, e):
        font = self.userLB.font()
        font.setUnderline(False)
        self.userLB.setFont(font)
        return super().leaveEvent(e)

    # 用户设置配置方法
    def setting(self):
        self.statusBar().showMessage('进入配置页')
        self.setting = ConfigChildWindow()
        self.setting.show()

    def changePath(self):
        save_path = config_manager.get('save_path')
        path = QFileDialog.getExistingDirectory(self, '选择下载目录', save_path)
        config_manager.set('save_path', value=path)
        config_manager.save()
        self.pathLB.setText(path)

    # 查询书籍
    def query(self):
        bookname = self.bookEdit.text()
        accrate_ = True if self.accurateCheck.isChecked() else False
        modes = {'默认': None, '热度': 'popular', '匹配度': 'bestmatch', '名称': 'title', '上传日期': 'date',
                 '出版日期': 'year'}
        extens = {'所有': None, 'AZW': 'AZW', 'AZW3': 'AZW3', 'MOBI': 'MOBI', 'EPUB': 'EPUB', 'PDF': 'PDF',
                  'TXT': 'TXT'}
        mode_ = modes[self.modeBox.currentText()]
        ext = extens[self.brBox.currentText()]

        log.info("开始搜索")
        self.getbooks = ZlibSearcherV3(bookname,mode=mode_,extension=ext,accurate=accrate_)
        self.getbooks.success.connect(self.show_book)
        self.getbooks.start()
        self.page = 1

    def next_page(self):
        if self.page == 0:
            QMessageBox.warning(self, "查询错误", "请先点击搜索")
        else:
            print("下一页")
            self.page += 1
            self.clear_book_view()
            self.getbooks.page += 1
            self.getbooks.start()

    def pre_page(self):
        if self.page <= 1:
            QMessageBox.warning(self, "查询错误", "上一页无内容")
        else:
            self.page -= 1
            self.clear_book_view()
            self.getbooks.page -= 1
            self.getbooks.start()


    def show_book(self, books):
        self.books_list = books

        if books is None:
            item_title = QTableWidgetItem("本次搜索无结果，请换一本书")
            self.tableWidget.setRowCount(1)
            self.tableWidget.setItem(0, 0, item_title)
        else:
            log.info(f"前端接收到{len(books)}本书,开始展示")
            self.tableWidget.setRowCount(len(books))
            self.reset_bookview_size()
            for row in range(len(books)):
                title = books[row]['title']
                author = books[row]['author']
                year = books[row]['year']
                extension = books[row]['file_type']
                filesize = books[row]['file_size']

                item_title = QTableWidgetItem(title)
                item_year = QTableWidgetItem(year)
                item_extension = QTableWidgetItem(extension)
                item_size = QTableWidgetItem(filesize)
                item_author = QTableWidgetItem(author)

                self.tableWidget.setItem(row, 0, item_title)
                self.tableWidget.setItem(row, 1, item_author)
                self.tableWidget.setItem(row, 2, item_year)
                self.tableWidget.setItem(row, 3, item_extension)
                self.tableWidget.setItem(row, 4, item_size)
        self.search_state = 0

    def clear_book_view(self):
        self.tableWidget.setRowCount(20)
        self.reset_bookview_size()
        for row in range(20):
            item_title = QTableWidgetItem("")
            item_year = QTableWidgetItem("")
            item_extension = QTableWidgetItem("")
            item_size = QTableWidgetItem("")
            item_author = QTableWidgetItem("")
            self.tableWidget.setItem(row, 0, item_title)
            self.tableWidget.setItem(row, 1, item_author)
            self.tableWidget.setItem(row, 2, item_year)
            self.tableWidget.setItem(row, 3, item_extension)
            self.tableWidget.setItem(row, 4, item_size)

    def generateMenu(self, pos):
        # 获取点击行号，书籍序号
        path = config_manager.get('save_path')
        row_num = -1
        for i in self.tableWidget.selectionModel().selection().indexes():
            row_num = i.row()
        bookurl = self.books_list[row_num]['bookurl']
        # 使用正则表达式提取所需的部分
        match = re.search(r'/\d+/[a-f0-9]+', bookurl)
        # 获取匹配结果
        downid = match.group(0) if match else None
        title = self.books_list[row_num]['title']
        extension = self.books_list[row_num]['file_type']

        if row_num < 500:  # 表格生效的行数，501行点击右键，不会弹出菜单
            menu = QMenu()  # 实例化菜单
            item1 = menu.addAction(u"开始下载")
            action = menu.exec_(self.tableWidget.mapToGlobal(pos))
        else:
            return

        if action == item1:
            log.info(f"开始下载{title}.{extension}")
            self.clickDownload(downid, title, extension)
        else:
            return

    def reset_bookview_size(self):
        width = self.tableWidget.size().width()
        rate1 = 320 / 674
        rate2 = 80 / 674
        self.tableWidget.setColumnWidth(0, int(width * rate1))
        self.tableWidget.setColumnWidth(1, int(width * rate2))
        self.tableWidget.setColumnWidth(2,int(width * rate2))
        self.tableWidget.setColumnWidth(3, int(width * rate2))
        self.tableWidget.setColumnWidth(4, int(width * rate2))

    def reset_downlist_size(self):
        self.tableWidgetDownload.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def find_me(self):
        webbrowser.open("https://space.bilibili.com/19276680")

def main():
    app = QApplication(sys.argv)
    olib = MainWindow()
    olib.show()
    sys.exit(app.exec_())


# 主函数
if __name__ == '__main__':
    # PyQt5的固定用法
    app = QApplication(sys.argv)
    olib = MainWindow()
    olib.show()
    sys.exit(app.exec_())
