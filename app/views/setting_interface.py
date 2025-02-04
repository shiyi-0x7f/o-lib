# coding:utf-8
import webbrowser

from qfluentwidgets import (SettingCardGroup, SwitchSettingCard,
                            OptionsSettingCard, RangeSettingCard, PushSettingCard,
                             HyperlinkCard, PrimaryPushSettingCard, ScrollArea,
                           ExpandLayout, InfoBar, CustomColorSettingCard,setThemeColor)
from qfluentwidgets import FluentIcon as FIF
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget,QFileDialog
from loguru import logger
from ..common.config import cfg, HELP_URL,AUTHOR, VERSION, YEAR
from ..common.style_sheet import StyleSheet
from ..utils import CheckUpdate

class SettingInterface(ScrollArea):
    """ Setting interface """
    def __init__(self, obj_name,parent=None):
        super().__init__(parent=parent)
        self.setObjectName(obj_name)
        self.scrollWidget = QWidget()
        self.expandLayout = ExpandLayout(self.scrollWidget)
        # personalization
        self.personalGroup = SettingCardGroup(self.tr('个性化'), self.scrollWidget)
        self.themeColorCard=CustomColorSettingCard(
            cfg.themeColor,
            FIF.PALETTE,
            "主题色",
            "调整应用主题色",
            self.personalGroup
        )
        self.zoomCard = OptionsSettingCard(
            cfg.dpiScale,
            FIF.ZOOM,
            "界面缩放",
            "调整组件和字体大小",
            texts=[
                "100%", "125%", "150%", "175%", "200%",
                "使用系统设置"
            ],
            parent=self.personalGroup
        )
        #
        # # searchDown
        self.searchDownGroup = SettingCardGroup(self.tr('搜索&下载设置'), self.scrollWidget)
        self.downloadSwitchCard = SwitchSettingCard(
            FIF.DOWNLOAD,
            "下载开关",
            "应对某些地区网络受限的情况",
            configItem=cfg.downloadSwitch,
            parent=self.searchDownGroup
        )

        self.repeatFilesCard = SwitchSettingCard(
            FIF.FILTER,
            "重名文件选项",
            "自动重命名会在文件末尾增加时间戳",
            configItem=cfg.reapeatFiles,
            parent=self.searchDownGroup
        )
        self.repeatFilesCard.switchButton.checkedChanged.connect(self.repeatFilesHandle)
        button = self.repeatFilesCard.switchButton
        isChecked = button.isChecked()
        text = self.tr('跳过') if isChecked else self.tr(
            '自动重命名')
        button.setText(text)

        self.onlinePageSizeCard = RangeSettingCard(
            cfg.searchNums,
            FIF.SEARCH,
            "展示数",
            "每次搜索结果的展示数量",
            parent=self.searchDownGroup
        )
        self.downloadFolderCard = PushSettingCard(
            "选择文件夹",
            FIF.FOLDER,
            "当前下载文件夹",
            cfg.get(cfg.downloadFolder),
            self.searchDownGroup
        )

        # update software
        self.updateSoftwareGroup = SettingCardGroup("检查更新", self.scrollWidget)
        self.updateOnStartUpCard = SwitchSettingCard(
            FIF.UPDATE,
            "应用启动时检查更新",
            "强制更新时该选项无效。",
            configItem=cfg.checkUpdateAtStartUp,
            parent=self.updateSoftwareGroup
        )

        # application
        self.aboutGroup = SettingCardGroup("关于", self.scrollWidget)
        self.helpCard = HyperlinkCard(
            HELP_URL,
            "打开帮助页",
            FIF.HELP,
            "帮助",
            parent=self.aboutGroup
        )
        self.gitCard = PrimaryPushSettingCard(
            "开源地址",
            FIF.GITHUB,
            "开源地址",
            "开源图书Open Library(Olib),让更多的人无门槛获得知识~",
            self.aboutGroup
        )
        self.gitCard.button.clicked.connect(self.__git)

        self.homeCard = PrimaryPushSettingCard(
            "拾壹的主页",
            FIF.HOME,
            "你可以发现",
            "我是什么样的人，我做了哪些事儿~",
            self.aboutGroup
        )
        self.homeCard.button.clicked.connect(self.__home)

        latest_ver = "手动更新" if cfg.latestVersion.value is None else cfg.latestVersion.value
        self.aboutCard = PrimaryPushSettingCard(
            "检查更新",
            FIF.INFO,
            "版权信息",
            f"Olib ©{YEAR} {AUTHOR}. 当前版本{VERSION} 最新版本{latest_ver}\n"
            f"PyQt-Fluent-Widgets ©{YEAR}  zhiyiyo",
            self.aboutGroup
        )
        self.aboutCard.button.clicked.connect(self.__check_update)

        self.__initWidget()
        # StyleSheet.SETTING_INTERFACE.apply(self)

    def repeatFilesHandle(self):
        button = self.repeatFilesCard.switchButton
        isChecked = button.isChecked()
        text = self.tr('跳过') if isChecked else self.tr('自动重命名')
        button.setText(text)
        logger.info(f"设置为{text}")
        cfg.set(cfg.reapeatFiles,isChecked)
    def __check_update(self):
        cu = CheckUpdate()
        cu.handle_version()
        logger.info("点击检查更新")

    def __git(self):
        webbrowser.open("https://github.com/shiyi-0x7f/o-lib")

    def __home(self):
        webbrowser.open("https://www.11xy.cn")

    def __initWidget(self):
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)

        # initialize layout
        self.__initLayout()
        self.__connectSignalToSlot()

    def __initLayout(self):
        # add cards to group
        self.personalGroup.addSettingCard(self.themeColorCard)
        self.personalGroup.addSettingCard(self.zoomCard)

        self.searchDownGroup.addSettingCard(self.onlinePageSizeCard)
        self.searchDownGroup.addSettingCard(self.repeatFilesCard)
        self.searchDownGroup.addSettingCard(self.downloadSwitchCard)
        self.searchDownGroup.addSettingCard(self.downloadFolderCard)

        self.updateSoftwareGroup.addSettingCard(self.updateOnStartUpCard)


        self.aboutGroup.addSettingCard(self.homeCard)
        self.aboutGroup.addSettingCard(self.helpCard)
        self.aboutGroup.addSettingCard(self.gitCard)
        self.aboutGroup.addSettingCard(self.aboutCard)

        # add setting card group to layout
        self.expandLayout.setSpacing(28)
        self.expandLayout.addWidget(self.personalGroup)
        self.expandLayout.addWidget(self.searchDownGroup)
        self.expandLayout.addWidget(self.updateSoftwareGroup)
        self.expandLayout.addWidget(self.aboutGroup)

    def __showRestartTooltip(self):
        """ show restart tooltip """
        InfoBar.warning(
            '设置成功',
            "重启软件后生效",
            duration=1500,
            parent=self
        )
    def __onDownloadFolderCardClicked(self):
        """ download folder card clicked slot """
        folder = QFileDialog.getExistingDirectory(
            self, self.tr("Choose folder"), "./")
        if not folder or cfg.get(cfg.downloadFolder) == folder:
            return

        cfg.set(cfg.downloadFolder, folder)
        self.downloadFolderCard.setContent(folder)

    def __connectSignalToSlot(self):
        cfg.appRestartSig.connect(self.__showRestartTooltip)
        self.themeColorCard.colorChanged.connect(setThemeColor)
        self.downloadFolderCard.clicked.connect(self.__onDownloadFolderCardClicked)
