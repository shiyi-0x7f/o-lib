# _*_ coding:utf-8 _*_
# Copyright (C) 2023-2023 shiyi0x7f,Inc.All Rights Reserved
# @Time : 2023/6/7 20:20
# @Author: shiyi0x7f
# get请求线程类
from PyQt5.QtCore import pyqtSignal,QThread
import time
import requests
from loguru import logger as log
try:
    from OlibFluent.app.utils import get_domain,get_uuid
except:
    from ..utils import get_domain,get_uuid
class OlibSearcherV4(QThread):
    sig_success = pyqtSignal(list)
    sig_fail = pyqtSignal(int)
    def __init__(self,bookname,languages=None,extensions=None,page=None,order="bestmatch",limit="100",e=None,yearFrom=None,yearTo=None):
        super(OlibSearcherV4, self).__init__()
        self.page = page
        self.bookname = bookname
        self.languages = languages
        self.extensions = extensions
        self.order = order
        self.limit = limit
        self.e = e
        self.yearFrom = yearFrom
        self.yearTo = yearTo
        self.pagination = None
    def run(self):
        self.book_from_my_api()  # 初始化书籍传输列表

    def book_from_my_api(self):
        t1 = time.time()
        domain = get_domain()
        api_search = f'{domain}/getbooks'
        log.info(f"{api_search} 当前第{self.page}页")
        json_data = {
            "bookname": self.bookname,
            "page": self.page,
            "languages": self.languages,
            "extensions": self.extensions,
            "order": self.order,
            "limit": self.limit,
            "e": self.e,
            "yearFrom": self.yearFrom,
            "yearTo": self.yearTo
        }
        headers = {"UUID": get_uuid()}
        resp = requests.post(api_search,json=json_data,headers=headers)
        log.info(f"从服务端接收到数据,耗时{time.time() - t1:.2f}s")
        if resp.status_code == 429:
            self.sig_fail.emit(999) #速率限制提示
            return
        data = resp.json()
        try:
            if data['success']==1:
                books = data['books']
                if books:
                    log.success("数据接收成功,开始传送数据")
                    self.pagination = data['pagination']
                    self.sig_success.emit(books)
                else:
                    log.warning("数据为空")
                    self.sig_fail.emit(0) #0表示成功接收,但是数据为空
            else:
                log.warning(f"数据接收失败,{data}")
                self.sig_fail.emit(-1) #-1代表未知异常
        except Exception as e:
            self.sig_fail.emit(-999) #-999 搜索词预警



if __name__ == '__main__':
    zs = OlibSearcherV4("三体",languages=["english"],limit="10",e="1")
    res = zs.book_from_my_api()
    print(res)