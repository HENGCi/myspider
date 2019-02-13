# -*- coding: utf-8 -*-
import scrapy


class TellthetruthSpider(scrapy.Spider):
    name = 'tellthetruth'
    allowed_domains = ['news.ifeng.com']
    start_urls = ['http://news.ifeng.com/']
    '''
    资讯 --> 讲真
    '''
    def parse(self, response):
        # filename = 'tellthetruth.html'
        # with open(filename,'wb') as fp:
        #     fp.write(response.body)

        links = response.xpath('*').re(r'"data":.*?"url":"(.*?)",')

        for url in links :

            yield  scrapy.Request(url=url,callback=self.second)

    def second(self,response):
        filename = 'tdetail.html'

        with open(filename,'wb')as fp:

            fp.write(response.body)




