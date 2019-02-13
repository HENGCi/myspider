# -*- coding: utf-8 -*-
import scrapy
from ifeng.items import NewsItem
class NewsSpider(scrapy.Spider):
    name = 'news'
    allowed_domains = ['news.ifeng.com']
    start_urls = ['http://news.ifeng.com/xijinping/']
    '''
    资讯-->新时代
    '''
    def parse(self, response):
        # filename = 'news.html'
        # with open(filename,'wb') as fp:
        #     fp.write(response.body)

        link_list = response.xpath('*').re(r'"(https://news.ifeng.com/c/.*?)"')

        link_set = set(link_list)

        self.log(len(link_set))

        for url in link_set:
            self.log('当前url:%s'%url)
            yield  scrapy.Request(url=url,callback=self.second)


    def second(self,response):

        # filename = 'detail.html'
        #
        # with open(filename,'wb') as fp:
        #
        #     fp.write(response.body)

        title = response.xpath('*').re_first('docData":.*?"title":"(.*?)",')

        pubtime = response.xpath('*').re_first('docData":.*?"newsTime":"(.*?)",')

        source = response.xpath('*').re_first('docData":.*?"source":"(.*?)",')

        content = response.xpath('*').re_first('docData":.*?"data":"(.*?)",')

        author =  response.xpath('*').re_first('docData":.*?"editorName":"(.*?)",')

        editorCode = response.xpath('*').re_first('docData":.*?"editorCode":"(.*?)",')

        item = NewsItem(
            title=title,
            pubtime=pubtime,
            source=source,
            content=content,
            author=author,
            editorCode=editorCode
        )

        yield item


        #写文件
        # filename = 'data.txt'
        #
        # with open(filename,'w',encoding='utf-8') as fp:
        #
        #     fp.write(title+'\n'+pubtime+'\n'+source+'\n')


