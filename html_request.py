#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import re
class Html_request(object):
    header = {
        'Host':'www.dianping.com',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0',
        'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Referer':'https://www.dianping.com/citylist'
    }
    header1 = {
        'Host':'www.dianping.com',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0',
        'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Origin':'https://www.dianping.com',
        }
    cookie = {
        "_dp.ac.v":"f7247ae4-03fb-462b-b123-2a06c1144c83","_hc.v":"8e8a5ffc-dd8e-6323-a91b-bdc3c5d0b914.1567697995","_lx_utm":"utm_source=Baidu&utm_medium=organic","_lxsdk":"16d0215047ec8-0d62f883f871918-4c312272-1fa400-16d0215047fb4","_lxsdk_cuid":"16d0215047ec8-0d62f883f871918-4c312272-1fa400-16d0215047fb4","_lxsdk_s":"171d0858e0e-f59-e45-06e||137","cityid":"4","ctu":"0ad8c845e1e160ce8781a3f5d0c27f52c8f79b2008a485450a163c1c2759c57b","cy":"4","cye":"guangzhou","dper":"34b2dba6dd95c0919affa6d285d41eeaeffc96c4099844904d2609ab7ad387beca78698d63df31932bdf60a3c44375e5cbffa6cee56509d0c5ca203fbe002132e27830197def5b28731d551d05eb131e8394f1b5c933e15461ab2025c13d1ae3","dplet":"8b1ecb24336d12093d6af489d3457001","fspop":"test","lgtoken":"0a129de15-61a2-4410-9a41-f0f16b3c0db9","ll":"7fd06e815b796be3df069dec7836c3df","s_ViewType":"10","switchcityflashtoast":"1","t_lxid":"171c6901a1921-03ae255a3c33d58-4c302e7f-1fa400-171c6901a1ac8-tid","ua":"è¦ç¶ä¸¶éç¶","uamo":"17329948370"
    }
    def __init__(self,city):
        self.city2 = city
    def get_city_id(self):
        city_link = "https://www.dianping.com/"+self.city2
        res = requests.get(city_link,headers=self.header,cookies=self.cookie)
        # r.headers 为服务器响应的cookies
        response_cookie = res.headers
        key = re.compile(r"cy=(\d+)")
        result = key.findall(response_cookie['Set-Cookie'])
        return result[0]
    
    def get_search_result(self,link):
        _res = requests.get(link,headers=self.header1,cookies=self.cookie).content
        return _res

# 用法：
#obj = Search_city_id('foshan')
#a = obj.get_city_id()
