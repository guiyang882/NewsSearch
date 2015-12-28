#!/bin/bash

cd ../News_Scrapy/News_Scrapy/ 
rm /tmp/scrapy.log
touch /tmp/scrapy.log
nohup scrapy crawl "News_Scrapy" --logfile=/tmp/scrapy.log 2>&1 &
