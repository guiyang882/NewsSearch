#!/usr/bin/env python
# coding=utf-8

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from News_Scrapy.items import NewsScrapyItem
from scrapy.conf import settings
from scrapy.http import Request
import os,pickle,json
#import signal
import sys,types,re
from bs4 import BeautifulSoup
import jieba.analyse

## MySelf define the Global Variable
SAVED_URL = set()
if os.path.isfile(settings["SAVED_URL_PATH"]):
    with open(settings["SAVED_URL_PATH"],"rb") as handle:
        SAVED_URL = pickle.load(handle)

def save_url_pkl(sig,frame):
    with open(settings["SAVED_URL_PATH"],"wb") as handle:
        pickle.dump(SAVED_URL,handle)
    sys.exit(0)

#signal.signal(signal.SIGINT,save_url_pkl)

class NetEaseSpider(CrawlSpider):
    name = "News_Scrapy"
    allowed_domains = ["news.163.com"]
    start_urls = ["http://news.163.com","http://news.163.com/domestic/","http://news.163.com/world/","http://news.163.com/shehui/","http://war.163.com/","http://gov.163.com/"]
    rules = [
        Rule(SgmlLinkExtractor(allow=(r'http://[a-z]+.163.com/[a-z]*')),callback="parse_item"),
        Rule(SgmlLinkExtractor(allow=(r'http://[a-z]+.163.com/[0-9]{2}/[0-9]{3,4}/[0-9]{1,2}/[a-zA-Z0-9]+.html')),callback="parse_item_yield"),
    ]
    detail_re = re.compile(r'http://[a-z]+.163.com/[0-9]{2}/[0-9]{3,4}/[0-9]{1,2}/[a-zA-Z0-9]+.html')
    head_re = re.compile(r'http://[a-z]+.163.com')

    def parse_item(self,response):
        if response.url not in SAVED_URL:
            SAVED_URL.add(response.url)
            soup = BeautifulSoup(response.body)
            for item in soup.findAll("a"):
                if item.has_attr("href"):
                    head_url_list = re.findall(self.head_re,item["href"])
                    detail_url_list = re.findall(self.detail_re,item["href"])
                    if type(head_url_list) != types.NoneType:
                        for tmp in head_url_list:
                            if tmp not in SAVED_URL:
                                yield Request(tmp,callback=self.parse_item_yield)
                    if type(detail_url_list) != types.NoneType:
                        for tmp in detail_url_list:
                            if tmp not in SAVED_URL:
                                yield Request(tmp,callback=self.parse_item_yield)


    def parse_item_yield(self,response):
        if response.url not in SAVED_URL:
            SAVED_URL.add(response.url)
            soup = BeautifulSoup(response.body)
            news_item = NewsScrapyItem()
            news_item["news_title"] = u"网易新闻"
            if type(soup.find("title")) != types.NoneType:
                news_item["news_title"] = soup.find("title").string
            new_date_list = soup.findAll("div",{"class":["ep-time-soure cDGray","pub_time"]}) 
            news_date_re = re.findall(r"\d{2}/\d{4}/\d{2}",response.url)[0].split("/")
            news_item["news_date"] = "20" + news_date_re[0] + "-" + news_date_re[1][:2] + "-" + news_date_re[1][-2:] + " " + news_date_re[2]
            if len(new_date_list) != 0:
                news_item["news_date"] = new_date_list[0].string[:19]
            tmp_news_source = soup.find("a",{"id":"ne_article_source"})
            if tmp_news_source != None:
                news_item["news_source"] = tmp_news_source.string
            else:
                news_item["news_source"] = "NetEase"
            data = soup.findAll("div",{"id":"endText"})[0]
            data_list = data.findAll("p",{"class":""})
            contents = ""
            for item in data_list:
                if type(item.string) != types.NoneType:
                    test = item.string.encode("utf-8")
                    contents = contents + test
            news_item["news_content"] = contents
            key_map = {}
            for x,w in jieba.analyse.extract_tags(contents,withWeight=True):
                key_map[x] = w
            news_item["news_key"] = json.dumps(key_map)
            yield news_item

            for item in soup.findAll("a"):
                if item.has_attr("href"):
                    head_url_list = re.findall(self.head_re,item["href"])
                    detail_url_list = re.findall(self.detail_re,item["href"])
                    if type(head_url_list) != types.NoneType:
                        for tmp in head_url_list:
                            if tmp not in SAVED_URL:
                                yield Request(tmp,callback=self.parse_item_yield)
                    if type(detail_url_list) != types.NoneType:
                        for tmp in detail_url_list:
                            if tmp not in SAVED_URL:
                                yield Request(tmp,callback=self.parse_item_yield)
    
