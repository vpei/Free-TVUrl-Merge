#!/usr/bin/env python3

import requests
import re
import json
import base64
import urllib.parse

class IsValid(): # 将订阅链接中YAML，Base64等内容转换为 Url 链接内容
    
    # 检测文本是否是BASE64格式
    def isBase64(s):
        try:
            _base64_code = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',
                            'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
                            'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a',
                            'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
                            'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                            't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1',
                            '2', '3', '4','5', '6', '7', '8', '9', '+',
                            '/', '=' ]
            # Check base64 OR codeCheck % 4
            code_fail = [ i for i in s if i not in _base64_code]
            if code_fail or len(s) % 4 != 0:
                return False
            return True
        except Exception as ex:
            print('Line-43: is_base64_code(s) err: ' + str(ex) + '\n' + s)
            return False
           
    pattern = re.compile(
        r'^(([a-zA-Z]{1})|([a-zA-Z]{1}[a-zA-Z]{1})|'
        r'([a-zA-Z]{1}[0-9]{1})|([0-9]{1}[a-zA-Z]{1})|'
        r'([a-zA-Z0-9][-_.a-zA-Z0-9]{0,61}[a-zA-Z0-9]))\.'
        r'([a-zA-Z]{2,13}|[a-zA-Z0-9-]{2,30}.[a-zA-Z]{2,3})$'
    )
    # 检测文本是否是域名格式
    def isDomain(domain):
        """ 
        Return whether or not given value is a valid domain.
        If the value is valid domain name this function returns ``True``, otherwise False
        :param value: domain string to validate
        """
        return True if pattern.match(domain) else False
        
    # 检测文本是否是IP格式
    def isIP(strIp):
      try:
        p = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
        if p.match(strIp):
            return True
        else:
            return False
      except:
        return False
        
    def isIPorDomain(strs):
        if(len(strs) > 0):
            if(strs.find('.') > -1):
                return True
            else:
                return False
        else:
            return False

    # str.isnumeric()