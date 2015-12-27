#-*- coding:utf-8 -*-

import web
import MySQLdb
import json

from DBUtils import PooledDB

urls = (
    "/","index"
)

pool = PooledDB.PooledDB(creator=MySQLdb,maxusage=50,host="localhost",user="root",passwd="root",db="user",charset='utf8')

class index:
    def GET(self):        
        web.header('Access-Control-Allow-Origin','*')
        web.header('Content-Type','application/json')
        befor_data = web.input()
        data = None
        if befor_data.has_key("CONTENTS"):
            if befor_data["CONTENTS"] == "MANAGERS":
                data = self.getManagersInfo()
            if befor_data["CONTENTS"] == "CONSUMERS":
                data = self.getConsumerInfo()
            if befor_data["CONTENTS"] == "MESSAGELOG":
                being_id = int(befor_data["begin"])
                end_id = int(befor_data["end"])
                data = self.getMessageLogInfo(being_id,end_id)
                total_length = self.getMessageLogLength()
                data["total_length"] = total_length
            if befor_data["CONTENTS"] == "USERNAMES":
                data = self.getAllUserName()
            if befor_data["CONTENTS"] == "FILTERUSER":
                data = self.getUserSendLog(befor_data["NAME"])

        if befor_data.has_key("operator"):
            if befor_data["operator"] == "consumers-deleted":
                self.delete_consumers_info(befor_data)
                data = self.getConsumerInfo()
            if befor_data["operator"] == "managers-deleted":
                self.delete_managers_info(befor_data)
                data = self.getManagersInfo()
            if befor_data["operator"] == "UpdateUserInfo":
                data = self.updateUserInfo(befor_data["old_info"],befor_data["update_info"])

        return json.dumps(data)
    
    def POST(self):
        web.header('Access-Control-Allow-Origin','*')
        web.header('Access-Control-Allow-Headers', 'content-type')
        web.header('Content-Type','application/json')
        print web.input()
        data = self.getdata()
        return data
   
    def OPTIONS(self):
        web.header('Access-Control-Allow-Origin','*')
        web.header('Access-Control-Allow-Headers', 'content-type')
        web.header('Content-Type','application/json')
        return 
   
    def updateUserInfo(self,old_info,new_info):
        old_info = json.loads(old_info)
        new_info = json.loads(new_info)
        db = pool.connection()
        cursor = db.cursor()
        print old_info['name']
        sql_del = "delete from t_user where name='%s';" % old_info['name']
        cursor.execute(sql_del)
        sql_insert = "insert into t_user(name,wx_id,phone,other_info,status,comments) values ('%s','%s','%s','%s',%d,'%s');"
        sql_insert = sql_insert % (new_info[0],new_info[1],new_info[2],new_info[3],int(new_info[4]),new_info[5])
        print sql_insert
        cursor.execute(sql_insert)
        cursor.close()
        db.close()

    def delete_consumers_info(self,info):
        db = pool.connection()
        cursor = db.cursor()
        name = info["name"]
        sql_del = "delete from t_user where name='%s';" % (name)
        print sql_del
        cursor.execute(sql_del)
        cursor.close()
        db.close()
       
    def delete_managers_info(self,info):
        db = pool.connection()
        cursor = db.cursor()
        name = info["name"]
        sql_del = "delete from t_manage_user where name='%s';" % (name)
        print sql_del
        cursor.execute(sql_del)
        cursor.close()
        db.close()

    def getConsumerInfo(self):
        db = pool.connection()
        cursor = db.cursor()
        sql_exec = "select * from t_user;"
        cursor.execute(sql_exec)
        data = cursor.fetchall()
        cursor.close()
        db.close()
        result = {'name':'UserInfo',"data":[]}
        info_list = []
        #| name  | wx_id  | phone  | other_info | status | comments  |
        for item in data:
            info_map = {}
            info_map["name"] = item[0]
            info_map["wx_id"] = item[1]
            info_map["phone"] = item[2]
            info_map["other_info"] = item[3]
            info_map["status"] = item[4]
            info_map["comments"] = item[5]
            info_list.append(info_map)
        result["data"] = info_list
        return result
    
    def getManagersInfo(self):
        db = pool.connection()
        cursor = db.cursor()
        sql_exec = "select * from t_manage_user;"
        cursor.execute(sql_exec)
        data = cursor.fetchall()
        cursor.close()
        db.close()
        result = {"name":"ManagersInfo","data":[]}
        info_list = []
        #| name | wx_id | phone | other_info | status | comments
        for item in data:
            info_map = {}
            info_map["name"] = item[0]
            info_map["wx_id"] = item[1]
            info_map["phone"] = item[2]
            info_map["other_info"] = item[3]
            info_map["status"] = item[4]
            info_map["comments"] = item[5]
            info_list.append(info_map)
        result["data"] = info_list
        return result

    def getMessageLogInfo(self,begin,end):
        db = pool.connection()
        cursor = db.cursor()
        sql_exec = "select * from t_send_log where id>=%d and id<=%d ;" % (int(begin),int(end))
        print sql_exec
        cursor.execute(sql_exec)
        data = cursor.fetchall()
        cursor.close()
        db.close()
        result = {"name":"MessageLog","data":[]}
        info_list = []
        for item in data:
            info_map = {}
            info_map['id'] = item[0]
            info_map["from"] = item[1]
            info_map['to'] = item[2]
            info_map['mode'] = item[3]
            info_map['time'] = item[4]
            info_map['contents'] = item[5]
            info_list.append(info_map)
        result["data"] = info_list
        return result

    def getMessageLogLength(self):
        db = pool.connection()
        cursor = db.cursor()
        sql_exec = "select count(*) from t_send_log;"
        cursor.execute(sql_exec)
        data = cursor.fetchall()
        cursor.close()
        db.close()
        return int(data[0][0])

    def getAllUserName(self):
        db = pool.connection()
        cursor = db.cursor()
        sql_exec = "select distinct name from t_user;"
        cursor.execute(sql_exec)
        data = cursor.fetchall()
        cursor.close()
        db.close()
        result = {"name":"UserNames","data":[]}
        info_list = []
        for item in data:
            info_list.append(item[0])
        result["data"] = info_list
        return result

    def getUserSendLog(self,name):
        db = pool.connection()
        cursor = db.cursor()
        sql_exec = "select * from t_send_log where to_user='%s';" % name
        print sql_exec
        cursor.execute(sql_exec)
        data = cursor.fetchall()
        cursor.close()
        db.close()
        result = {"name":"UserSendLog","data":[]}
        info_list = []
        for item in data:
            info_map = {}
            info_map["id"] = item[0]
            info_map["from"] = item[1]
            info_map["to"] = item[2]
            info_map["mode"] = item[3]
            info_map["time"] = item[4]
            info_map["contents"] = item[5]
        result["data"] = info_list
        return result

if __name__ == "__main__":
    web.config.debug = False
    app = web.application(urls,globals())
    app.run()


