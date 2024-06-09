# _*_ coding:utf-8 _*_
# Copyright (C) 2024-2024 shiyi0x7f,Inc.All Rights Reserved
# @Time : 2024/6/4 下午1:15
# @Author: shiyi0x7f
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
import sys
from config_window_func import LoginChildWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")
        self.setGeometry(100, 100, 800, 600)

        self.button = QPushButton('Open Login Window', self)
        self.button.setGeometry(100, 100, 200, 50)
        self.button.clicked.connect(self.open_login_window)

    def open_login_window(self):
        self.login_window = LoginChildWindow()
        self.login_window.user_data.connect(
            self.handle_login_data)
        self.login_window.sig_downnum.connect(
            self.handle_downnum)
        self.login_window.exec_()

    def handle_login_data(self, data):
        if data:
            print("Login data received:", data)
        else:
            print("Login failed")

    def handle_downnum(self, num):
        print("Down number:", num)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
