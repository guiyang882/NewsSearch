#-*- coding:utf-8 -*-

import MySQLdb
import string
import random
import datetime
import time

conn=MySQLdb.connect(host="localhost",user="root",passwd="root",db="user",charset="utf8")
cursor = conn.cursor()
def add_User():
    for i in range(0,50):
        random.seed(i)
        sql = "insert into t_user(name,wx_id,phone,other_info,status,comments) values ('%s','%s','%s','%s',1,'%s');"
        name = string.join(random.sample(['z','y','x','w','v','u','t','s','r','q','p','o','n','m','l','k','j','i','h','g','f','e','d','c','b','a'], 5)).replace(' ','')
        wx_id = str(random.randint(10000,500000))
        phone = string.join(random.sample(['1','2','3','4','5','6','7','8','9','0'],10)).replace(' ','')
        other_info = 'null'
        comments = 'hello gpx !!!'
        sql_exec =  sql % (name,wx_id,phone,other_info,comments)
        print sql_exec
        cursor.execute(sql_exec)

    conn.commit() 

def add_manage():
    for i in range(0,10):
        random.seed(i)
        sql = "insert into t_manage_user(name,wx_id,phone,other_info,status,comments) values ('%s','%s','%s','%s',1,'%s');"
        name = string.join(random.sample(['z','y','x','w','v','u','t','s','r','q','p','o','n','m','l','k','j','i','h','g','f','e','d','c','b','a'],5)).replace(' ','')
        wx_id = str(random.randint(1000000,2000000))
        phone = string.join(random.sample(['1','2','3','4','5','6','7','8','9','0'],10)).replace(' ','')
        other_info = name+"@gpxtrade.com"
        comments = string.join(random.sample(['admin','superuser','custom'],1)).replace(' ','')
        sql_exec = sql % (name,wx_id,phone,other_info,comments)
        print sql_exec
        cursor.execute(sql_exec)

    conn.commit()

def add_send_log():
    for i in range(0,1500):
        random.seed(i)
        sql = "insert into t_send_log (from_user,to_user,comm_mode,time,contents) values ('%s','%s','%s','%s','%s');"
        from_user = "【北京极派客】"
        to_user = string.join(random.sample(['z','y','x','w','v','u','t','s','r','q','p','o','n','m','l','k','j','i','h','g','f','e','d','c','b','a'],5)).replace(' ','')
        comm_mode = string.join(random.sample(['weixin','email','phone'],1)).replace(' ','')
        str_time = str(datetime.datetime.now())
        info = "【北京极派客】"+to_user+" 您好！"+"您的持股信息请求变更 ！！，相关信息请确认！！"
        time.sleep(1)
        sql_exec = sql % (from_user,to_user,comm_mode,str_time,info)
        print sql_exec
        cursor.execute(sql_exec)

if __name__ == "__main__":
    add_send_log()
    cursor.close()
    conn.close()
    print "Sql Data insert Over !!"


