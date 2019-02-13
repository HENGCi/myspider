import requests
from lxml import etree
import json
import re

def index():
    url = 'http://www.ifeng.com/'

    headers = {
        'Hos': 'www.ifeng.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache'
    }

    try:
        response = requests.get(url=url, headers=headers)

        response.raise_for_status()

    except Exception:

        response = None

    elem = etree.HTML(response.text)

    print(elem.xpath('//div[@class="wrap NavMCon"]/ul[@class="clearfix"]/li/a/@href'))


def second():
    url = 'http://news.ifeng.com/'

    headers = {
        'Host': 'news.ifeng.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate',
        # Referer: http://www.ifeng.com/
        'Connection': 'keep-alive',
        'Cache-Control': 'no-cache'
    }

    try:
        response = requests.get(url=url, headers=headers)

        response.raise_for_status()
    except Exception:

        response = None

    if response is not None:

        # print(response.text)

        result = re.search(r'.*"topNav":(.*?),"topNavId":30063',response.text)

        # print(result.groups(1)[0])

        link_list = json.loads(result.groups(1)[0])

        for i in link_list:
            url = i['url']
            print(url)

def third():
    url = 'http://news.ifeng.com/xijinping/'

    headers = {

    }

    try :
        response = requests.get(url=url,headers=headers)

        response.raise_for_status()

    except Exception:
        response = None

if __name__ == '__main__':

    # index()

    second()