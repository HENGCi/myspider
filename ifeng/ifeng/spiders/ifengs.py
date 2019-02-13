# -*- coding: utf-8 -*-
import scrapy


class IfengsSpider(scrapy.Spider):
    name = 'ifengs'
    allowed_domains = ['www.ifeng.com']
    start_urls = [
        'http://news.ifeng.com/',
       ]

    def parse(self, response):
        pass