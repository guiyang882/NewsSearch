#!/bin/bash

cd ../News_Scrapy/News_Scrapy/ 
nohup scrapy crawl "News_Scrapy" --logfile=/tmp/scrapy.log &
