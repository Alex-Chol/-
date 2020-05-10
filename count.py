import requests
import json
import math
from math import sin,radians,cos,asin,sqrt
class Count(object):
    def __init__(self):
        self.apikey = '9851491f89e236963cc842eb61570a68' # 高德地图API密钥
        self.data_type = 'json'  # 返回数据格式。可选xml与json
    def get_result(self,city,score,comment,price,adress,local_lat,local_lng,first,second,third,fouth,wish_price,m_comment,m_score):
        city = city+'市' # 在city参数传过来的值后面加上 市
        link = "https://restapi.amap.com/v3/geocode/geo?address="+city+adress+"&output="+self.data_type+"&key="+self.apikey
        r = requests.get(link)
        json_data = json.loads(r.text)
        location = json_data['geocodes'][0]['location']
        longitude,latitude = location.split(",") # 获取目标地址经纬度
        distance = self.haversine(float(local_lat),float(local_lng),float(latitude),float(longitude))
        return self.compute(float(distance),int(score),comment,float(price),first,second,third,fouth,float(wish_price),m_comment,m_score),distance
        

    def haversine(self,lat1,lng1,lat2,lng2): 
        "用haversine公式计算球面两点间的距离。"
        # 经纬度转换成弧度
        lng1, lat1, lng2, lat2 = map(radians, [lng1, lat1, lng2, lat2])
        dlon = lng2 - lng1
        dlat = lat2 - lat1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        r = 6371 # 地球平均半径，单位为公里
        return '%.2f'%(c * r * 1000)

    def compute(self,distance,score,comment,price,first,second,third,fouth,wish_price,m_comment,m_score):
        # 距离 点评数 评价 价格
        # 判断第一个参数
        if first == '距离':
            s1 = float(self.count_distance(distance))*0.4
        elif first == '点评数':
            s2 = float(self.count_comment(comment,m_comment))*0.4
        elif first == '评价':
            s3 = float(self.count_score(score,m_score))*0.4
        elif first == '价格':
            s4 = float(self.count_price(price,wish_price))*0.4
        # 判断第二个参数
        if second == '距离':
            s1 = float(self.count_distance(distance))*0.3
        elif second == '点评数':
            s2 = float(self.count_comment(comment,m_comment))*0.3
        elif second == '评价':
            s3 = float(self.count_score(score,m_score))*0.3
        elif second == '价格':
            s4 = float(self.count_price(price,wish_price))*0.3
        # 判断第三个参数
        if third == '距离':
            s1 = float(self.count_distance(distance))*0.2
        elif third == '点评数':
            s2 = float(self.count_comment(comment,m_comment))*0.2
        elif third == '评价':
            s3 = float(self.count_score(score,m_score))*0.2
        elif third == '价格':
            s4 = float(self.count_price(price,wish_price))*0.2      
        # 判断第四个参数
        if fouth == '距离':
            s1 = float(self.count_distance(distance))*0.1
        elif fouth == '点评数':
            s2 = float(self.count_comment(comment,m_comment))*0.1
        elif fouth == '评价':
            s3 = float(self.count_score(score,m_score))*0.1
        elif fouth == '价格':
            s4 = float(self.count_price(price,wish_price))*0.1
        return '%.6f' %(s1+s2+s3+s4)
        

    def count_distance(self,distance):
        return "%.6f" %(1/(1+math.fabs(math.log(distance))))
    
    def count_comment(self,comment,m_comment):
        return '%.6f' %((1+comment-m_comment[0])/(m_comment[1]-m_comment[0]))
    
    def count_score(self,score,m_score):
        return '%.6f' %((1+score-m_score[0])/(1+m_score[1]-m_score[0]))

    def count_price(self,price,wish_price):
        return '%.6f' %(1/(1+math.fabs(wish_price-price)))
# a = Count()
# print(a.get_result("佛山",5,5296,120,"南海区中海锦城","23.13171","113.26627","点评数","价格","评价","距离",50,[120,9999],[2,5]))

