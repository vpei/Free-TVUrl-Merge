#!/usr/bin/env python3

import os
import time

class TimeText(): # 将订阅链接中YAML，Base64等内容转换为 Url 链接内容
    # 读取本地文件的修改时间
    def get_local_file_modifiedtime(fname):
        try:
            modifiedTime = time.localtime(os.stat(fname).st_mtime)
            #mTime = time.strftime('%Y-%m-%d %H:%M:%S', modifiedTime)
            return time.asctime(modifiedTime)
        except Exception as ex:
            print("Line-35-local_file: get local file modified time error. \n" + str(ex))
            return 0

    # 读取本地文件的创建时间
    def get_local_file_created_time(fname):
        try:
            createdTime = time.localtime(os.stat(fname).st_ctime)
            #cTime = time.strftime('%Y-%m-%d %H:%M:%S', createdTime)
            return createdTime
        except Exception as ex:
            print("Line-45-local_file: get local file modified time error. \n" + str(ex))
            return 0
