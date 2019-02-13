# -*- coding: utf-8 -*-
import scrapy
import json
from weibo.items import UserItem,WeiboItem,UserRelationItem
class WeibouserSpider(scrapy.Spider):
    name = 'weibouser'
    allowed_domains = ['m.weibo.cn']
    '''
        关注url :https://m.weibo.cn/api/container/getIndex?containerid=231051_-_followers_-_2146892831&page=2
    '''
    start_users = [
        '2656274875',
        '2431328567',
    ]

    weibo_url = 'https://m.weibo.cn/api/container/getIndex?containerid=230413{uid}_-_WEIBO_SECOND_PROFILE_WEIBO&luicode=10000011&lfid=230283{uid}&type=uid&value={uid}&page_type=03&page={page}'

    user_url = 'https://m.weibo.cn/api/container/getIndex?uid={uid}&luicode=10000011&lfid=230413{uid}_-_WEIBO_SECOND_PROFILE_WEIBO&type=uid&value={uid}&containerid=100505{uid}'

    fans_url = 'https://m.weibo.cn/api/container/getIndex?containerid=231051_-_fans_-_{uid}&type=uid&value=5896763203&since_id={since_id}'

    follower_url = 'https://m.weibo.cn/api/container/getIndex?containerid=231051_-_followers_-_{uid}&type=uid&value={uid}&page={page}'

    def start_requests(self):
        for uid in self.start_users:
            yield scrapy.Request(url=self.user_url.format(uid=uid),callback=self.parse_user)

    def parse_user(self, response):

        result = json.loads(response.text)

        if result.get('data') and result.get('data').get('userInfo'):

            user_info = result.get('data').get('userInfo')
            item  = UserItem()
            field_map = {
                'id':'id',
                'name':'screen_name',
                'gender':'gender',
                'description':'description',
                'followers_count':'followers_count',
                'follow_count':'follow_count'
            }

            for k,v in field_map.items():
                item[k] = user_info[v]

            yield item

        # #关注
            uid = user_info.get('id')
            yield scrapy.Request(
                url=self.follower_url.format(uid=uid,page=1),
                callback=self.parse_follow,
                meta={'uid':uid,'page':1}
            )

        #微博
            yield scrapy.Request(
                url=self.weibo_url.format(uid=uid,page=1),
                callback=self.parse_weibo,
                meta={'page':1,'uid':uid}
            )
        #粉丝
            yield scrapy.Request(
                url=self.fans_url.format(uid=uid,since_id=1),
                callback=self.parse_fans,
                meta={'uid':uid,'since_id':1}
            )


    #微博解析
    def parse_weibo(self,response):

        result = json.loads(response.text)

        if result.get('data') and result.get('data').get('cards'):

            weibo_list = result.get('data').get('cards')
            item = WeiboItem()
            field_map = {
                'created_at':'created_at',
                'id':'id',
                # 'attitudes_count':'attitudes_count',
            }
            for weibo in weibo_list:

                if weibo.get('mblog'):
                    mblog = weibo.get('mblog')
                    for k,v in field_map.items():
                        item[k] = mblog[v]

                yield item
        #下一页微博
        uid = response.meta.get('uid')
        page = response.meta.get('page')+1
        self.log(uid)
        yield scrapy.Request(
            url=self.weibo_url.format(uid=uid,page=page),
            callback=self.parse_weibo,
            meta={'page':page,'uid':uid}
        )







    # 关注解析
    def parse_follow(self,response):

        result = json.loads(response.text)

        if result.get('data').get('cards'):

            # cards = result.get('data').get('cards')

            #解析出用户信息
            follows = result.get('data').get('cards')[-1].get('card_group')
            for follow in follows:
                if follow.get('user'):
                    uid = follow.get('user').get('id')
                    yield scrapy.Request(self.user_url.format(uid=uid),callback=self.parse_user)
            item = UserRelationItem()
            #解析关注用户信息
            uid = response.meta.get('uid')
            followers = [{'id':follow.get('user').get('id'),'name':follow.get('user').get('screen_name'),} for follow in follows]

            item['id'] = uid
            item['follows'] = followers
            item['fans'] = []
            yield item
        #下一页关注列表
            page = response.meta.get('page')+1
            yield scrapy.Request(
                url=self.follower_url.format(uid=uid,page=page),
                callback=self.parse_follow,
                meta={'page':page,'uid':uid}
            )

    def parse_fans(self, response):

        result = json.loads(response.text)

        if result.get('data').get('cards'):

            fans = result.get('data').get('cards')[-1].get('card_group')

            for fan in fans :
                if fan.get('user'):
                    uid = fan.get('user').get('id')
                    yield scrapy.Request(
                        url=self.user_url.format(uid=uid),
                        callback=self.parse_user,
                    )
            fanser = [{'id':fan.get('user').get('id'),'name':fan.get('user').get('screen_name')} for fan in fans]

            item = UserRelationItem()
            uid = response.meta.get('uid')
            item['id'] = uid
            item['fans'] = fanser
            item['follows'] = []
            yield item
            #下一页粉丝
            since_id = response.meta.get('since_id')+1
            yield scrapy.Request(
                url=self.fans_url.format(uid=uid,since_id=since_id),
                callback=self.parse_fans,
                meta={'since_id':since_id,'uid':uid}
            )


