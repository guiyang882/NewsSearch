# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo

from scrapy.exceptions import DropItem
from scrapy.conf import settings
from scrapy import log

class NewsScrapyPipeline(object):
    #Connect to the MongoDB database
    def __init__(self):
        connection = pymongo.Connection(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        #Remove invalid data
        valid = True
        for data in item:
          if not data:
            valid = False
            raise DropItem("Missing %s of blogpost from %s" %(data, item['url']))
        if valid:
            new_moive=[{
                "news_date":item['news_date'],
                "news_title":item['news_title'],
                "news_source":item['news_source'],
                "news_content":item['news_content'],
                "news_key":item['news_key']
            }]
            list_res = list(self.collection.find({"news_title":item["news_title"]}))
            if len(list_res) == 0:
                self.collection.insert(new_moive)
                log.msg("Item wrote to MongoDB database %s/%s" % (settings['MONGODB_DB'], settings['MONGODB_COLLECTION']),
                level=log.DEBUG, spider=spider) 
        return item

