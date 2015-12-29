#!/usr/bin/env python
# coding=utf-8

import pymongo
import json
import pickle

connection = pymongo.Connection("127.0.0.1",27017)
db = connection["python"]
cursor = db["test"]

def load_News_DB():
    contents = cursor.find({},{"news_title":1,"news_key":1,"_id":0})
    index = 0
    key_index_map = {}
    for item in contents:
        index = index + 1
        if item.has_key("news_key"):
            news_key_str = item["news_key"]
            news_key = json.loads(news_key_str)
            for word in news_key.keys():
                if word.isdigit() == False:
                    if key_index_map.has_key(word):
                        key_index_map[word].append((item["news_title"],news_key[word]))
                    else:
                        key_index_map[word] = [(item["news_title"],news_key[word])]
        if index % 10000 == 0:
            with open("index_"+str(index) + ".json",'w') as handle:
                for tmp in key_index_map.keys():
                    tmp_list = sorted(key_index_map[tmp],key = lambda x:x[1],reverse = False)
                    key_index_map[tmp] = []
                    for title in tmp_list:
                        key_index_map[tmp].append(title[0])
                handle.write(json.dumps(key_index_map))
            key_index_map = {}

    with open("index_"+str(index) + ".json",'w') as handle:
        for tmp in key_index_map.keys():
            tmp_list = sorted(key_index_map[tmp],key = lambda x:x[1],reverse = False)
            key_index_map[tmp] = []
            for title in tmp_list:
                key_index_map[tmp].append(title[0])
        handle.write(json.dumps(key_index_map))

def load_News_DB_pkl():
    contents = cursor.find({},{"news_title":1,"news_key":1,"_id":0})
    index = 0
    key_index_map = {}
    for item in contents:
        index = index + 1
        if item.has_key("news_key"):
            news_key_str = item["news_key"]
            news_key = json.loads(news_key_str)
            for word in news_key.keys():
                if word.isdigit() == False:
                    if key_index_map.has_key(word):
                        key_index_map[word].append((item["news_title"],news_key[word]))
                    else:
                        key_index_map[word] = [(item["news_title"],news_key[word])]
        if index % 10000 == 0:
            with open("index_"+str(index) + ".pkl",'w') as handle:
                for tmp in key_index_map.keys():
                    tmp_list = sorted(key_index_map[tmp],key = lambda x:x[1],reverse = False)
                    key_index_map[tmp] = []
                    for title in tmp_list:
                        key_index_map[tmp].append(title[0])
                pickle.dump(key_index_map,handle)
            key_index_map = {}

    with open("index_"+str(index) + ".pkl",'w') as handle:
        for tmp in key_index_map.keys():
            tmp_list = sorted(key_index_map[tmp],key = lambda x:x[1],reverse = False)
            key_index_map[tmp] = []
            for title in tmp_list:
                key_index_map[tmp].append(title[0])
        pickle.dump(key_index_map,handle)

if __name__ == "__main__":
    #load_News_DB()
    load_News_DB_pkl()
