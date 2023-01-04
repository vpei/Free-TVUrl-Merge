#!/usr/bin/env python3

import datetime
import os

class LocalFile(): # 将订阅链接中YAML，Base64等内容转换为 Url 链接内容

    # 从本地文本文件中读取字符串
    def read_LocalFile(fname):
        retxt = ""
        try:
            with open(fname, "r", encoding='utf-8') as f:  # 打开文件
                retxt = f.read()  # 读取文件
        except Exception as ex:
            print('LocalFile-Line-15-Exception:\n' + str(ex))
        return retxt

    # 写入字符串到本地文件
    def write_LogFile(fcont):
        print(fcont)
        fname = './tmp/err.log'
        if(fcont.find('Exception') == -1):
            fname = './tmp/info.log'
        fcont = '[' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '] ' + fcont
        LocalFile.write_LocalFile(fname, fcont)

    # 写入字符串到本地文件
    def write_LocalFile(fname, fcont):
        try:
            # 创建目录 # os.makedirs(os.path.split(fname)[0])
            if(fname.find('/') > -1):
                dirs = fname.rsplit('/', 1)[0]
                if not os.path.exists(dirs):
                    os.makedirs(dirs)            
            # ”w"代表着每次运行都覆盖内容 #只需要将之前的”w"改为“a"即可，代表追加内容
            wtype = 'w'
            if(os.path.exists(fname)):
                fsize = os.path.getsize(fname) # 文件路径及文件名
                if(fname.find('.log') > -1 and fsize < 80000000):
                    fcont = '\n\n' + fcont
                    wtype = 'a'
            else:
                fsize = len(fcont)
            # 内容格式转换
            _file = open(fname, wtype, encoding='utf-8')
            _file.write(fcont.encode("utf-8").decode("utf-8"))
            _file.close()
            if(fcont.find('Exception') > -1):
                print('LocalFile-Line-49-Write-OK-Type(a-add,w-write): ' + wtype + '-Size:' + str(fsize) + '-Path:' + fname)
        except Exception as ex:
            print('LocalFile-Line-46-write-Exception:\n' + str(ex) + '\nPath:' + fname + '-Fcont:' + fcont)