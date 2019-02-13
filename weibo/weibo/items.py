# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

from scrapy import Field

class UserItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    collection = 'user'

    id = Field()
    name = Field()
    gender = Field()
    description = Field()
    followers_count = Field()
    follow_count = Field()
    crawled_at = Field()

class UserRelationItem(scrapy.Item):

    collection = 'user'
    id = Field()
    follows = Field()
    fans = Field()


class WeiboItem(scrapy.Item):

    collection = 'weibos'
    id = Field()
    attitudes_count = Field()
    comments_count = Field()
    reposts_count = Field()
    picture = Field()
    pictures = Field()
    source = Field()
    texte = Field()
    raw_texte = Field()
    thumbnaile = Field()
    usere = Field()
    created_at = Field()
    crawled_at = Field()


