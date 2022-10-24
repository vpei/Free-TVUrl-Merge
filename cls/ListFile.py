#!/usr/bin/env python3

import requests
import os
import time

class ListFile(): # 将订阅链接中YAML，Base64等内容转换为 Url 链接内容
 
    def get_list_sort(s):
        global list
        # 先将列表转化为set，再转化为list就可以实现去重操作
        list = list(set(s))
        # 将list进行排序 .sort(reverse=True)表示倒序
        list.sort()
        return list