# -*- coding: utf-8 -*-
import scrapy

from ifeng.items import PhotoItem
class PhotoSpider(scrapy.Spider):
    name = 'photo'
    allowed_domains = [
        'photo.ifeng.com',
        'news.ifeng.com'
    ]
    start_urls = ['https://photo.ifeng.com/']
    '''
    资讯 --> 图片
    '''
    def parse(self, response):
        # filename = 'imgindex.html'
        # with open(filename,'wb') as fp:
        #
        #     fp.write(response.body)

        index_links = response.xpath('*').re(r'"title2":.*?"url":"(.*?)"')

        for url in index_links:
            yield scrapy.Request(url=url,callback=self.second)

    def second(self,response):


        image_links = response.xpath('*').re('"thumbnail":"(.*?)","title"')

        item = PhotoItem()

        for i in image_links:

            self.log('当前图片url:%s'%i)

        item['image_urls'] = ['https://p3.ifengimg.com/a/2017_04/5e04b25f5b41f9a.png']

        yield  item
