# _*_ coding:utf-8 _*_
# Copyright (C) 2024-2024 shiyi0x7f,Inc.All Rights Reserved
# @Time : 2024/12/4 下午9:19
# @Author: shiyi0x7f
from PyQt5.QtWidgets import QApplication
from app.utils import setup_logger
from app.common.config import cfg
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from app.views.main_window import Window
import sys
import os
from loguru import logger


if __name__ == '__main__':
    setup_logger()
    if cfg.get(cfg.dpiScale) == "Auto":
        QApplication.setHighDpiScaleFactorRoundingPolicy(
            Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
        QApplication.setAttribute(
            Qt.AA_EnableHighDpiScaling)
    else:
        os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "0"
        os.environ["QT_SCALE_FACTOR"] = str(
            cfg.get(cfg.dpiScale))
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    # create application
    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings)

    # create main window
    w = Window()
    w.setWindowIcon(QIcon(":/image/ICO"))
    w.show()

    sys.exit(app.exec_())