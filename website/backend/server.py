#-*- coding:utf-8 -*-

import web
import json

urls = (
    "/","index"
)

class index:
    def GET(self):
        web.header('Access-Control-Allow-Origin','*')
        web.header('Content-Type','application/json')
        befor_data = web.input()
        data = None
        if befor_data.has_key("CONTENTS"):
            if befor_data["CONTENTS"] == "SEARCH":
                key_info = befor_data["QUERY"]
                if len(key_info) == 0:
                    return json.dumps({"name":"search","code":"1","status":"No Query Word"})
                data = self.search_related(key_info)

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

    def search_related(self,key_word):
        result = {'name':'search',"data":[]}
        return result

if __name__ == "__main__":
    web.config.debug = False
    app = web.application(urls,globals())
    app.run()


