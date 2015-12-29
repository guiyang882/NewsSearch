#!/usr/bin/env python
# coding=utf-8

import pymongo
import json

connection = pymongo.Connection("127.0.0.1",27017)
db = connection["python"]
cursor = db["test"]

key_index_map = {}

def load_News_DB():
    contents = cursor.find({},{"news_title":1,"news_key":1,"_id":0})
    for item in contents:
        if item.has_key("news_key"):
            news_key_str = item["news_key"]
            news_key = json.loads(news_key_str)
            for word in news_key.keys():
                if word.isdigit() == False:
                    if key_index_map.has_key(word):
                        key_index_map[word].append((item["news_title"],news_key[word]))
                    else:
                        key_index_map[word] = [(item["news_title"],news_key[word])]
    with open("index.json",'w') as handle:
        handle.write(json.dumps(key_index_map))

if __name__ == "__main__":
    load_News_DB()
