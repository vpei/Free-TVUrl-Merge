#!/usr/bin/env python3

class StrText():

    # Base64加密文本转换为标准格式
    def get_str_base64(origStr):
        missing_padding = 4 - len(origStr) % 4 
        if missing_padding: 
            origStr += '=' * missing_padding
        return origStr

    # 从字符中取两不同字符串中间的字符，print(sub_link)，参数：文本，第一字符串，第二字符串，是否保留字符串
    def get_str_btw(s, f, b, y):
        par = s.partition(f)
        if(y == 0):
            return (par[2].partition(b))[0][:]
        else:
            return f + '' + (par[2].partition(b))[0][:] + '' + b

    # 大小换算
    def bytes_conversion(self, number: float):
        """
        换算大小
        :param number: byte字节单位
        :return: 大小
        """
        symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
        prefix = dict()
        for a, s in enumerate(symbols):
            prefix[s] = 1 << (a + 1) * 10
        for s in reversed(symbols):
            if int(number) >= prefix[s]:
                value = float(number) / prefix[s]
                return '%.1f%s/s' % (value, s)
        return "%sB/s" % number

	def hum_convert(value):
	    value=float(value)
	    units = ["B", "KB", "MB", "GB", "TB", "PB"]
	    size = 1024.0
	    for i in range(len(units)):
	        if (value / size) < 1:
	            return "%.2f%s" % (value, units[i])
	        value = value / size

    #检验是否全是中文字符
    def is_all_chinese(strs):
        for _char in strs:
            if not '\u4e00' <= _char <= '\u9fa5':
                return False
        return True

    #检验是否含有中文字符
    def is_contains_chinese(strs):
        for _char in strs:
            if '\u4e00' <= _char <= '\u9fa5':
                return True
        return False
		