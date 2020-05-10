import pymysql
import json
class Connent_mysql(object):
    def __init__(self):
        self.conn = pymysql.connect(host='47.100.78.99',port=3306,user='root',passwd='',db='dianping',charset='utf8')
        self.cursor=self.conn.cursor() # 获得游标
    
    def mysql_insert(self,name,address,score,comment,price,img,total_score,distance):
        try:
            self.cursor.execute("insert into result values('"+name+"', '"+address+"', '"+score+"', '"+comment+"', '"+price+"', '"+img+"', '"+total_score+"', '"+distance+"')")
        except Exception:
            pass
        self.conn.commit()
 

    def mysql_select(self,sort):
        a = 0
        dic = {}
        if sort == '1':
            self.cursor.execute('select * from result order by distance ASC')
        elif sort == '2':
            self.cursor.execute('select * from result order by score DESC')
        elif sort == '3':
            self.cursor.execute('select * from result order by comment DESC')
        elif sort == '4':
            self.cursor.execute('select * from result order by total_score DESC')

        data = self.cursor.fetchall()
        for each in data:
            dis = '%.3f' %(float(each[7])*0.001)
            value = {"name":each[0],"address":each[1],"score":each[2],"comment":each[3],"price":each[4],"img":each[5],"distance":dis}
            dic[a] = value
            a += 1
        print(json.dumps(dic))
        #print(json.loads(json.dumps(dic)))

    def mysql_delete(self):
        self.cursor.execute('delete from result')
        self.conn.commit()

    def mysql_close(self):
        self.cursor.close()
        self.conn.close()

# a = Connent_mysql()
# a.mysql_insert('海底捞火锅(奥体南路店)', '奥体南路12号奥体购物中心市场C203A、C203B号', '五星商户', '771', '￥121', 'null')
# a.mysql_select()
# a.mysql_close()

