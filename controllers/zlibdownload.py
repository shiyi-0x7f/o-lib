# _*_ coding:utf-8 _*_
# Copyright (C) 2023-2023 shiyi0x7f,Inc.All Rights Reserved
# @Time : 2023/6/7 22:39
# @Author: shiyi0x7f
from PyQt5.QtCore import QThread,pyqtSignal,QMutex
from utils.config import config_manager
from utils.log import log
from bs4 import BeautifulSoup
import time
import requests
import os
import re
down_lock = QMutex()
class ZlibDownloader3(QThread):
    sig_down_process = pyqtSignal(QThread,int)  # 下载量信号 list: value flag
    speed = pyqtSignal(QThread,float)
    final = pyqtSignal(bool)
    def __init__(self,bookid,bookname,extension):
        super().__init__()
        self.bookid = bookid
        self.name = bookname.replace(':',"")
        self.extension = extension
        self.base_url = config_manager.get('base_url')
        self.path = config_manager.get('save_path')
        self.remix_id = config_manager.get('remix_id')
        self.remix_key = config_manager.get('remix_key')

        self.cookies = {
            'siteLanguageV2': 'zh',
            'remix_userid': self.remix_id,
            'remix_userkey': self.remix_key,
        }

        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'priority': 'u=0, i',
            'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
        }

    def get_down_id(self):
        # 使用正则表达式提取所需的部分
        bookid = self.bookid.split('/')[1]
        url = f'{self.base_url}/papi/book/{bookid}/formats'
        with requests.get(url,cookies=self.cookies, headers=self.headers) as response:
            try:
                if response.json().get('books'):
                    down_id = response.json()['books'][0]['href']
                else:
                    down_id = self.get_down_url_from_page()
                log.success(f'获取down_id成功,{down_id}')
                return down_id
            except Exception as e:
                print(response.json())
                log.error(f"获取down_id失败:{e}")

    def get_down_url_from_page(self):
        try:
            url = f"{self.base_url}/book{self.bookid}"
            response = requests.get(url,cookies=self.cookies, headers=self.headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            response.close()
            down_id = soup.find('a',class_='addDownloadedBook premiumBtn')['href']
            log.success(f"获取下载id成功")
            return down_id
        except Exception as e:
            log.error(f"获取下载id失败{e}")

    def get_down_url(self):
        downid = self.get_down_id()
        url = f'{self.base_url}{downid}'
        params = {
            'dsource': 'recommend',
        }
        with requests.get(url,params=params,
            cookies=self.cookies,
            headers=self.headers,
            allow_redirects=True) as response:
            if response.url:
                log.success(f"获取下载地址成功{response.url}")
                return response.url
            else:
                log.error(f"获取下载地址失败:{response.text}")
                return False



    def run(self):#run中不带返回值
        down_lock.lock()
        try:
            durl = self.get_down_url()
            response = requests.get(durl, cookies=self.cookies,headers=self.headers, allow_redirects=True,stream=True)
            chunk_size = 1024
            read = 0
            the_filename = self.name + "." + self.extension
            the_sourceFile = os.path.join(self.path, the_filename)

            with open(f"{the_sourceFile}", 'ab') as f:
                file_size = int(response.headers.get('content-length', 0))
                start_time = time.time()
                print("文件大小",file_size)

                for chunk in response.iter_content(chunk_size=chunk_size):
                    f.write(chunk)
                    read += chunk_size
                    read = min(read,file_size)
                    current_time = time.time()+1
                    dspeed =read//1024/(current_time-start_time)
                    if current_time-start_time>1:
                        self.speed.emit(self,round(dspeed,2))
                    self.progressToEmit(int(read / file_size * 100))
            response.close()
            self.final.emit(True)
        except Exception as e:
            log.error(f"下载失败：{e}")
            self.final.emit(False)
        finally:
            down_lock.unlock()

    def progressToEmit(self, iProgress):
        self.sig_down_process.emit(self, iProgress)



if __name__ == '__main__':
    def handle_progress(self, thread, value):
        print(f"Progress: {value}%")


    def handle_speed(self, thread, speed):
        print(f"Speed: {speed} KB/s")


    def handle_final(self, success):
        if success:
            print("Download completed successfully")
        else:
            print("Download failed")

    zd = ZlibDownloader3("/23995486/e9c020","三体","epub")
    #zd.get_down_url_from_page()
    zd.sig_down_process.connect(handle_progress)
    zd.speed.connect(handle_speed)
    zd.final.connect(handle_final)
    zd.start()
    zd.wait()  # 等待线程执行完毕