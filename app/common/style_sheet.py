# coding: utf-8
from enum import Enum
from qfluentwidgets import StyleSheetBase, Theme, isDarkTheme, qconfig
from PyQt5.QtCore import QFile,QTextStream
class StyleSheet(StyleSheetBase, Enum):
    """ Style sheet  """

    DOWNLOAD_INTERFACE = "download_interface"
    SETTING_INTERFACE = "setting_interface"
    SEARCH_INTERFACE = "search_interface"
    MAIN_WINDOW = "main_window"

    def path(self, theme=Theme.AUTO):
        theme = qconfig.theme if theme == Theme.AUTO else theme
        qss_path = f":/qss/{theme.value.upper()}"
        return qss_path
