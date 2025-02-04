# _*_ coding:utf-8 _*_
# Copyright (C) 2025-2025 shiyi0x7f,Inc.All Rights Reserved
# @Time : 2025/1/8 下午8:07
# @Author: shiyi0x7f
import psutil
import uuid

def get_first_mac():
    interfaces = psutil.net_if_addrs()
    for interface, addrs in interfaces.items():
        for addr in addrs:
            # 查找以MAC地址格式出现的接口
            if addr.family == psutil.AF_LINK:
                return addr.address

def get_uuid():
    namespace = uuid.NAMESPACE_DNS
    mac = get_first_mac()
    UUID = uuid.uuid5(namespace, mac)
    return str(UUID)

if __name__ == '__main__':
    uid = get_uuid()
    print(uid)