# _*_ coding:utf-8 _*_
# Copyright (C) 2023-2023 shiyi0x7f,Inc.All Rights Reserved
# @Time : 2023/6/7 20:20
# @Author: shiyi0x7f
# get请求线程类
from PyQt5.QtCore import pyqtSignal,QThread,QMutex
from bs4 import BeautifulSoup
from utils.config import config_manager
from utils.log import log

import requests

search_lock = QMutex()
class ZlibSearcherV3(QThread):  # 线程1
    '''
    v3版本
    搜索->获取书籍id->获取下载id->获取直链接
    '''
    success = pyqtSignal(object)
    def __init__(self,name, mode=None, accurate: bool = False, extension=None,y=0):
        super(ZlibSearcherV3, self).__init__()
        self.page = 1
        self.host = config_manager.get("base_host")
        self.remix_id = config_manager.get('remix_id')
        self.remix_key = config_manager.get('remix_key')

        self.name = name
        self.accurate = accurate
        self.extension = extension
        self.y = y
        self.mode = mode if mode else 'bestmatch'

    def set_url(self):
        url = f'https://{self.host}/'
        if self.accurate is True:  # 精确搜索
            self.surl = url + f's/?q="{self.name}"&e=1&order={self.mode}&page={self.page}'
        else:
            self.surl = url + f's/{self.name}?order={self.mode}&page={self.page}'

        if self.extension:  # 扩展名
            self.surl += f"&extensions%5B%5D={self.extension}"

    def run(self):
        search_lock.lock()
        self.UA = {"authority": self.host,
                   "method": "GET",
                   "scheme": "https",
                   "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                   "accept-language": "zh-CN,zh;q=0.9",
                   "cookie": f"siteLanguageV2=zh; remix_userkey={self.remix_key}; remix_userid={self.remix_id}; domains-availability=",
                   "sec-ch-ua-platform": "\"Windows\"",
                   "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
                   }
        self.set_url() #更新搜索链接

        books_list = []  # 初始化书籍传输列表
        books_list = self.book_from_zlib(self.surl)

        if len(books_list) == 0:
            log.warning("没有获取到书籍列表，请排查错误")
            self.success.emit(None)
        else:
            log.success("书籍列表获取成功,开始传送到前端")
            self.success.emit(books_list)
        search_lock.unlock()

    def book_from_zlib(self,surl):
        books = []
        resp = requests.get(surl).text
        soup = BeautifulSoup(resp, 'html.parser')

        result_box = soup.find('div', id='searchResultBox')  # 查找包含书籍信息的div
        bookItems = result_box.find_all('div', class_='resItemBoxBooks')  # 查找所有书籍信息的div
        for b in bookItems:
            book = {}
            title = b.find('z-cover')['title'] if b.find('z-cover')['title'] else 'N/A'
            bookurl = b.find('a')['href'] if b.find('a')['href'] else 'N/A'

            book_image_wrapper = b.find('img', class_='cover lazy')  # 查找封面图片容器元素
            if book_image_wrapper:
                book_image = book_image_wrapper.find('img')  # 查找封面图片元素
                thumbnail  = book_image_wrapper.get('data-src')
                if "not-exists" in thumbnail:
                    thumbnail = 'N/A'
            else:
                thumbnail = 'N/A'

            publisher_elem = b.find('div', class_='authors')  # 查找出版社元素
            publisher = publisher_elem.find('a').text.strip() if publisher_elem and publisher_elem.find('a') else 'N/A'


            author = b.find('z-cover')['author'] if b.find('z-cover')['author'] else 'N/A'

            year_elem = b.find('div', class_='property_year')  # 查找年份元素
            year = year_elem.find('div', class_='property_value').text.strip() if year_elem and year_elem.find('div',
                                                                                                               class_='property_value') else 'N/A'

            language_elem = b.find('div', class_='property_language')  # 查找语言元素
            language = language_elem.find('div', class_='property_value').text.strip() if language_elem and language_elem.find(
                'div', class_='property_value') else 'N/A'

            file_info_elem = b.find('div', class_='property__file')  # 查找文件信息元素
            file_info = file_info_elem.find('div',
                                            class_='property_value').text.strip() if file_info_elem and file_info_elem.find(
                'div', class_='property_value') else 'N/A'
            if file_info:
                file_type,file_size = file_info.split(',')
            else:
                file_size=None
                file_type=None

            book['title'] = title
            book['bookurl'] = bookurl
            book['thumbnail'] = thumbnail
            book['publisher'] = publisher
            book['author'] = author
            book['year'] = year
            book['language'] = language
            book['file_type'] = file_type
            book['file_size'] = file_size
            books.append(book)
        return books
if __name__ == '__main__':
    zs = ZlibSearcherV3("岁月")
    bs = zs.run()