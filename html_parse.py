#!/usr/bin/env python
# -*- coding: utf-8 -*-
from lxml import etree
import re
from html_hack import Html_hack
from bs4 import BeautifulSoup
from count import Count
class Html_parse(object):
    def __init__(self):
        self.hack = Html_hack()
    def info_parse(self,res):
        res_text = res.decode("UTF-8")
        # 打印页面源代码
        #print(res_text) 
        # 将页面源代码保存到txt
        # with open('1.txt', 'w+',encoding='UTF-8') as f:
        #     f.write(res_text)
        #     f.close()
        # 获取页面上的加密css文件链接
        key = re.compile(r'href="//s3plus.sankuai.com/v1/(.+).css"')
        key2 = re.compile(r'href="//s3plus.meituan.net/v1/(.+).css"')
        css_file = key.findall(res_text)
        if len(css_file) == 0:
            css_file = key2.findall(res_text)
        css_file_link = "https://s3plus.sankuai.com/v1/"+css_file[0]+".css"
        # 向破解函数传入css链接，返回破解后的字符字典
        code_list = self.hack.run_hack(css_file_link)
        # 在页面响应上替换所有的加密数据。再用lxml爬取数据
        for each in range(10):
            res_text = res_text.replace(code_list[str(each)],str(each))
        soup = BeautifulSoup(res_text,'lxml')
        shop = soup.find_all('div',id='shop-all-list')[0]
        shop_list = shop.find_all('li')
        title = []
        address = []
        score = []
        comment_hack = []
        price_hack = []
        img_src = []
        for i in range(len(shop_list)):
            xml = etree.HTML(str(shop_list[i]))
            title.append(xml.xpath("//div[@class='tit']/a/h4/text()")[0])
            score_tmp = xml.xpath("//div[@class='star_icon']/span/@class")[0]
            key = re.compile(r'\d+')
            a = key.findall(score_tmp)[0]
            if a == '50':
                score.append(5)
            elif a == '45' or a == '40':
                score.append(4)
            elif a == '35' or a == '30':
                score.append(3)
            elif a == '25' or a == '20':
                score.append(2)
            elif a == '15' or a == '10':
                score.append(1)
            else:
                score.append(0)

            address.append(xml.xpath("//a[@class='o-map J_o-map']/@data-address")[0])
            img_src.append(xml.xpath("//div[@class='pic']/a/img/@src")[0])
            key_comment_and_price = re.compile(r'<b>(.+?)</b>')
            
            comment_and_price_unhack = key_comment_and_price.findall(str(shop_list[i]))
            key_result = re.compile(r"[\d+]")
            # 可以匹配到<b>里面的数字
            comment_unhack2 = key_result.findall(comment_and_price_unhack[0])  # comment_unhack[0]匹配点评数量
            comment_hack.append(int(''.join(comment_unhack2))) # 这里的comment_hack 列表元素必须为int型，否则返回结果后使用max与min函数会出错，在插入mysql时，需将元素转换为字符串

            price_unhack2 = key_result.findall(comment_and_price_unhack[1])  # comment_unhack[0]匹配人均价格
            price_hack.append(''.join(price_unhack2))
            #print(title," 地址：",address," 评分：",score," 点评数量：",comment_hack," 人均价格：￥",price_hack," 店铺图片链接：",img_src)
        return title,address,score,comment_hack,price_hack,img_src