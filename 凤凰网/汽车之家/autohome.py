import  requests

url = 'https://k.autohome.com.cn/ajax/getfeedIntelligent?pageIndex=1&pageSize=20&_appid=koubei&date=20180129'

try:
    response = requests.get(url=url)

    print(response.text)

except Exception:

    response = None
