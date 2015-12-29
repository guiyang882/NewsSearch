#-*- coding:utf-8 -*-

import web
import json,os
import pickle

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
        result["data"] = self.read_news_index(key_word)
        return result

    def read_news_index(self,key_word):
        base_dir = "../../News_Index/"
        title_list = []
        for filename in os.listdir(base_dir):
            if filename.endswith("pkl"):
                with open(base_dir + filename,"rb") as handle:
                    index_map = pickle.load(handle)
                    if index_map.has_key(key_word):
                        title_list.extend(index_map[key_word])
                        if len(title_list) >= 10:
                            break
        return title_list
            
    
if __name__ == "__main__":
    web.config.debug = False
    app = web.application(urls,globals())
    app.run()


