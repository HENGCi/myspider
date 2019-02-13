# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import re
import time
from weibo.items import UserItem,WeiboItem,UserRelationItem

#数据清洗
class WeiboPipeline(object):

    def parse_time(self, date):
        if re.match('刚刚',date):
            date = time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time()))

        if re.match('\d+分钟前',date):
            minute = re.match('(\d+)',date).group(1)
            date = time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time()-float(minute)*60))

        if re.match('\d+小时前',date):
            hours = re.match('(\d+)',date).group(1)
            date = time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time()-float(hours)*60*60))

        if re.match('昨天',date):
            date = re.match('昨天(.*)',date).group(1)
            date = time.strftime('%Y-%m-%d ',time.localtime()-24*60*60)+' '+date

        if re.match('\d{2}-\d{2}',date):
            date = time.strftime('%Y-',time.localtime())+date+'00:00'
        return  date

    def process_item(self, item, spider):

        if isinstance(item,WeiboItem):
            if item.get('created_at'):
                item['created_at'] = item['created_at'].strip()
                item['created_at'] = self.parse_time(item.get('created_at'))

        return item

#数据存储
class MongoDbPipeline(object):

    def __init__(self,mongo_uri,mongo_db):

        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls,crawler):

        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    def process_item(self,item,spider):

        if isinstance(item,UserItem) or isinstance(item,WeiboItem):

            if item:
                self.db[item.collection].update({'id':item.get('id')},{'$set':item},upsert=True)

        if isinstance(item,UserRelationItem):
            if item:
                self.db[item.collection].update(
                    {'id':item.get('id')},
                    {'$addToSet':
                        {
                        'follows':{'$each':item['follows']},
                        'fans':{'$each':item['fans']}
                        }
                    },
                    upsert=True
                )
        return item


    def open_spider(self,spider):
        #链接数据库
        self.client = pymongo.MongoClient(self.mongo_uri)
        #选择数据库
        self.db = self.client[self.mongo_db]
        #创建索引
        self.db[UserItem.collection].create_index([('id',pymongo.ASCENDING)])
        self.db[WeiboItem.collection].create_index([('id',pymongo.ASCENDING)])

    def close_spider(self,spider):
        self.client.close()


#记录抓取时间
class TimePipeline(object):
    def process_item(self,item,spider):
        if isinstance(item,UserItem) or isinstance(item,WeiboItem):

            now = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())

            item['crawled_at'] = now

        return item
