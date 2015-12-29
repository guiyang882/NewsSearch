## This file Save Search Index

### 创建索引
- 单个文件使用的内存有限，因此不能一次性将10W条记录都存储搬进内存
- 将新闻标题和新闻的关键字提取出来，并进行排序
- 将数据通过用户的关键字进行查询，或者进行最近似的匹配
- 并找到排名最高的新闻标题，从数据库中找出其对应的其他信息

### pkl文件，文件内的格式如下
```
{
  "Some Key Word":["news_title_high",...,"news_title_low"],
  "Some Key Word":["news_title_high",...,"news_title_low"],
  "Some Key Word":["news_title_high",...,"news_title_low"],
  "Some Key Word":["news_title_high",...,"news_title_low"],
  "Some Key Word":["news_title_high",...,"news_title_low"],
  "Some Key Word":["news_title_high",...,"news_title_low"],
  "Some Key Word":["news_title_high",...,"news_title_low"]
}
```
