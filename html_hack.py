#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from fontTools.ttLib import TTFont
import urllib
import re
import os


class Html_hack(object):
    header = {
        'Host': 's3plus.meituan.net',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0',
    }
    def __init__(self):
        self.file_name = 'code.woff'
        if(os.path.exists(self.file_name)):
            os.remove(self.file_name)


    def run_hack(self,hack_link):# 参数hack_link:爬取页面的css文件   破解字体编码
        r = requests.get(hack_link,headers=self.header)
        # 使用正则表达式 匹配出 woff文件链接
        key = re.compile(r'PingFangSC-Regular-shopNum";src:url\("(.+?).eot')
        result = 'https:'+key.findall(r.text)[0]+'.woff'
        urllib.request.urlretrieve(result,self.file_name)
        return self.code_change(self.file_name)

    def code_change(self,woff_name):# 传入一个woff文件
        code_list = {}
        font = TTFont(woff_name)
        #print(font['post'].extraNames)
        for each in range(2,12):
            hack_num = '&#x'+font['post'].extraNames[each].split('uni')[1]+';'
            if(each == 11):
                code_list['0'] = hack_num
                break
            elif (each != 11):
                code_list[str(each-1)] = hack_num
        #print(code_list)
        return code_list

# 加密字符示例：{'1': '&#xf66c;', '2': '&#xf4aa;', '3': '&#xf77d;', '4': '&#xe9fc;', '5': '&#xeb1d;', '6': '&#xf1e8;', '7': '&#xe3b1;', '8': '&#xf3b1;', '9': '&#xecf0;', '0': '&#xf3f9;'}&#xe3b1;', '8': '&#xf3b1;', '9': '&#xecf0;', '0': '&#xf3f9;'};

# import urllib.request
# url="http://www.dianping.com/shop/127857802"

# header1 = {
#     'Host':'www.dianping.com',
#     'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0',
#     'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
#         }
# file1=urllib.request.Request(url=url,headers=header1)
# file = urllib.request.urlopen(file1)
# print('获取当前url:',file.geturl() )
# 获取当前url : https://verify.meituan.com/v2/web/general_page?action=spiderindefence&requestCode=20b7a19ac8894e2eb3e42dae96591bf9&platform=1000&adaptor=auto&succCallbackUrl=https%3A%2F%2Foptimus-mtsi.meituan.com%2Foptimus%2FverifyResult%3ForiginUrl%3Dhttp%253A%252F%252Fwww.dianping.com%252Fshop%252F127857802&theme=dianping



