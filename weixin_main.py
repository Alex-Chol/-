#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import sys
from lxml import etree
from urllib.parse import quote
from html_request import Html_request
from html_parse import Html_parse
from xpinyin import Pinyin
from connect_sql import Connent_mysql
from count import Count

class Main_run(object):
    def __init__(self,city):
        self.req = Html_request(city)
        self.info = Html_parse()
        self.count = Count()
        self.mysql = Connent_mysql()
    def find(self,search_key,page,city,lat,lng,first,second,third,fouth,sign,price,sort):
        city_id = self.req.get_city_id()
        url_s = quote(search_key)
        # link 由 城市id 与 搜索关键词 组成
        if sign == 4:
            price1 = int(price)-20
            price2 = int(price)+20
            link = "https://www.dianping.com/search/keyword/"+city_id+"/0_"+url_s+'/p'+str(page)+'x'+str(price1)+'y'+str(price2)
        elif sign == 1:
            link = "https://www.dianping.com/search/keyword/"+city_id+"/0_"+url_s+'/p'+str(page)
        else:
            link = "https://www.dianping.com/search/keyword/"+city_id+"/0_"+url_s+'/o'+sort+'p'+str(page)
        #print(link)
        response = self.req.get_search_result(link)
        #title,address,score,comment_hack,price_hack,img_src
        title,address,score,comment_hack,price_hack,img_src = self.info.info_parse(response)
        # 获取 点评数量和评价的最大最小值
        m_comment = [min(comment_hack),max(comment_hack)]
        m_score = [min(score),max(score)]
        # 加权计算
        total_score = []
        distance_list = []
        for i in range(0,len(title)):
            t_score,distance = self.count.get_result(city,score[i],comment_hack[i],price_hack[i],address[i],lat,lng,first,second,third,fouth,price,m_comment,m_score)
            total_score.append(t_score)
            distance_list.append(distance)
        # 存储到数据库↓
        for i in range(0,len(title)):
            self.mysql.mysql_insert(title[i],address[i],str(score[i]),str(comment_hack[i]),price_hack[i],img_src[i],total_score[i],distance_list[i])


# & C:/Python/python.exe c:/Users/Shinelon/Desktop/资料/毕业论文/代码/weixin_main.py 广州 烤串 2 3 23.13171 113.26627 距离 点评数 评价 价格 50
# & C:/Python/python.exe c:/Users/Shinelon/Desktop/资料/毕业论文/代码/weixin_main.py 广州 烤串 1 1 23.13171 113.26627 40 30 20 10 50
a = sys.argv[1]  # 第一个参数代表 城市名
b = sys.argv[2]  # 第二个参数代表 搜索关键词
c = sys.argv[3]  # 第三个参数代表 页数
d = sys.argv[4]  # 第四个参数代表 排序方式
e = sys.argv[5]  # 第五个参数代表 纬度
f = sys.argv[6]  # 第六个参数代表 经度
g = sys.argv[7]  # 第七个参数代表 自定义排序第一个参数
h = sys.argv[8]  # 第八个参数代表 自定义排序第二个参数
i = sys.argv[9]  # 第九个参数代表 自定义排序第三个参数
j = sys.argv[10] # 第十个参数代表 自定义排序第四个参数
k = sys.argv[11] # 第十一个参数代表 期望价格

mysql = Connent_mysql()
mysql.mysql_delete()
pinyin = Pinyin()
city = pinyin.get_pinyin(a,'') # 将城市的中文转换成拼音
go = Main_run(city)
sort = '3'
if d == '4':
    sign = 4  # sign 负责标记排序方式是否为用户自定义权重排序 ，如果为2 ，即使用用户自定义排序
elif d == '1':
    sign = 1
elif d == '2':
    sign = 2
elif d == '3':
    sign = 3
    sort = '11'
go.find(b,c,a,e,f,g,h,i,j,sign,k,sort)
mysql.mysql_select(str(d))
mysql.mysql_close()

