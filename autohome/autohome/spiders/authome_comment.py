# -*- coding: utf-8 -*-
import scrapy


class AuthomeCommentSpider(scrapy.Spider):
    name = 'authome_comment'
    allowed_domains = ['k.autohome.com.cn']
    start_urls = ['http://k.autohome.com.cn/']

    def parse(self, response):
        pass
