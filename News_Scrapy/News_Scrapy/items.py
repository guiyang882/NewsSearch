# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    news_date = scrapy.Field()
    news_title = scrapy.Field()
    news_source = scrapy.Field()
    news_content = scrapy.Field()
    news_key = scrapy.Field()
