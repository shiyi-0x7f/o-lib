# _*_ coding:utf-8 _*_
# Copyright (C) 2024-2024 shiyi0x7f,Inc.All Rights Reserved
# @Time : 2024/12/4 下午10:04
# @Author: shiyi0x7f
# coding:utf-8
# coding:utf-8
import os
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon,QPixmap
from PyQt5.QtWidgets import QApplication,QStackedWidget, QHBoxLayout
from qfluentwidgets import (NavigationInterface, NavigationItemPosition,
                            toggleTheme,StyleSheetBase, Dialog, FluentWindow, NavigationAvatarWidget,SwitchButton,
                            Flyout,FlyoutView,FlyoutAnimationType,InfoBar,InfoBarPosition,InfoBarIcon,setCustomStyleSheet,
                            TeachingTip,TeachingTipTailPosition)
from qfluentwidgets import FluentIcon as FIF
from qframelesswindow import FramelessWindow, StandardTitleBar
from .searchInterface import SearchInterface
from .downloadInterface import DownloadInterface
from .setting_interface import SettingInterface
from ..common import resources
from ..common.style_sheet import StyleSheet
from ..common.config import cfg
from ..utils import CheckUpdate


class Window(FramelessWindow):
    def __init__(self):
        super().__init__()
        self.setObjectName("main_window")
        self.setTitleBar(StandardTitleBar(self))
        self.hBoxLayout = QHBoxLayout(self)
        self.navigationInterface = NavigationInterface(self, showMenuButton=True)
        self.stackWidget = QStackedWidget(self)
        # create sub interface
        self.searchInterface = SearchInterface("搜索页")
        self.searchInterface.sig_download_start.connect(self.start_download)
        self.downloadInterface = DownloadInterface("下载页")
        self.downloadInterface.finished.connect(self.download_result)
        self.downloadInterface.sig_rate_limit.connect(self.msg_rate_limit)
        self.downloadInterface.sig_start.connect(self.start_download_msg)
        self.settingInterface = SettingInterface("设置页")

        #check update
        self.checkUpdate()
        # initialize layout
        self.initLayout()
        # add items to navigation interface
        self.initNavigation()
        self.initWindow()
        StyleSheet.MAIN_WINDOW.apply(self)
    def checkUpdate(self):
        cu = CheckUpdate()
        if cfg.checkUpdateAtStartUp.value:
            cu.handle_version() #检查版本更新
        self.show_notice(cu.get_notice())

    def show_notice(self,notice):
        show = notice.get('show')
        title = notice.get('title')
        content = notice.get('content')
        if show:
            InfoBar.warning(title, content, Qt.Vertical,
                            True, 15000,
                            InfoBarPosition.TOP, self)


    def initLayout(self):
        self.hBoxLayout.setSpacing(0)
        self.hBoxLayout.setContentsMargins(0, self.titleBar.height(), 0, 0)
        self.hBoxLayout.addWidget(self.navigationInterface)
        self.hBoxLayout.addWidget(self.stackWidget)
        self.hBoxLayout.setStretchFactor(self.stackWidget, 1)

    def initNavigation(self):
        self.navigationInterface.setCollapsible(True)  # 禁止展开
        self.addSubInterface('搜索页',FIF.SEARCH,self.searchInterface)

        self.addSubInterface('下载页',FIF.DOWNLOAD,self.downloadInterface,routeKey="Download")


        self.navigationInterface.addSeparator()
        self.addSubInterface("赞赏",FIF.HEART,routeKey="Like",position=NavigationItemPosition.BOTTOM,onClick=self.showMessageBox,select=False)
        self.addSubInterface("更改主题颜色", FIF.CONSTRACT,
                             routeKey="Theme",
                             position=NavigationItemPosition.BOTTOM,
                             onClick=self.updateStyleSheet,
                             select=False)
        self.addSubInterface('设置页', FIF.SETTING,self.settingInterface,position=NavigationItemPosition.BOTTOM)
        self.stackWidget.currentChanged.connect(
            self.onCurrentInterfaceChanged)
        self.stackWidget.setCurrentIndex(0)

    def updateStyleSheet(self):
        toggleTheme(True)
        theme = cfg.theme.value

    def initWindow(self):
        self.resize(900, 700)
        self.setWindowIcon(QIcon('resource/logo.png'))
        self.setWindowTitle('Olib开源图书——一款永久免费的电子书软件')
        self.titleBar.setAttribute(Qt.WA_StyledBackground)
        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)


    def addSubInterface(self,text: str, icon, interface=None,routeKey=None, position=NavigationItemPosition.TOP,parent=None,onClick=None,select=False):
        """ add sub interface """
        def func():
            if onClick is not None:
                onClick()
            else:
                if interface is not None:
                    self.switchTo(interface)
            return None

        if interface is not None:
            self.stackWidget.addWidget(interface)
        self.navigationInterface.addItem(
            routeKey=interface.objectName() if interface is not None else routeKey,
            icon=icon,
            text=text,
            onClick=func,
            tooltip=text,
            position=position if position else NavigationItemPosition.TOP,
            parentRouteKey=parent.objectName() if parent else None,
            selectable=select
        )

    def start_download_msg(self,title):
        InfoBar.success(
            title="下载开始",
            content=f"{title}下载开始，可以前往下载页查看。",
            orient=Qt.AlignHCenter,
            isClosable=False,  # disable close button
            position=InfoBarPosition.TOP_RIGHT,
            duration=2000,
            parent=self
        )

    def msg_rate_limit(self,e):
        InfoBar.warning(
            title="下载限制",
            content="当前服务器压力过大，限制为5次/分钟，请1分钟后再尝试。",
            orient=Qt.AlignHCenter,
            isClosable=False,  # disable close button
            position=InfoBarPosition.TOP_RIGHT,
            duration=2000,
            parent=self
        )

    def start_download(self,data):
        bookid,hashid,bookname,extension,size = data
        self.downloadInterface.download(bookid,hashid,bookname,extension,size)

    def switchTo(self, widget):
        self.stackWidget.setCurrentWidget(widget)

    def onCurrentInterfaceChanged(self, index):
        widget = self.stackWidget.widget(index)
        self.navigationInterface.setCurrentItem(widget.objectName())

    def download_result(self,e,bookname):
        print(e,bookname)
        if e:
            InfoBar.success(
                title="下载成功",
                content=f"🎉{bookname}下载成功啦",
                isClosable=True,
                position=InfoBarPosition.BOTTOM,
                duration=1500,
                parent=self.searchInterface
            )
        else:
            InfoBar.error(
                title="下载失败",
                content=f"o(╥﹏╥)o {bookname}下载失败~",
                isClosable=True,
                position=InfoBarPosition.BOTTOM,
                duration=1500,
                parent=self.searchInterface
            )

    def showMessageBox(self):
        content = '''Olib一路走来，遇到了很多人
        而今又很幸运地遇见了你
        我们只希望尽一些绵薄之力
        让更多人在繁杂尘世有一本书相伴
        谢谢你的喜欢~
        '''

        TeachingTip.create(
            target=self,
            image=QPixmap(":/image/DONATE"),
            title="❤感谢❤",
            isClosable=True,
            content=content,
            duration=15000,
            tailPosition=TeachingTipTailPosition.RIGHT_BOTTOM
        )


if __name__ == '__main__':
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    w = Window()
    w.show()
    app.exec_()
