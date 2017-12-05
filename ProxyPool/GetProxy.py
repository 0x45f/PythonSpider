from lxml import html
import requests


class GetProxy:

    def __init__(self):
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Host': 'www.xicidaili.com',
            'Referer': 'http://www.xicidaili.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
        }
        self.__session = requests.session()
        self.__session.headers.update(headers)

    def get_tree(self, page):
        text = self.__session.get('http://www.xicidaili.com/nn/' + str(page)).text
        # print(text)
        return html.fromstring(text)

    def get_proxy(self, tree):
        trs = tree.xpath('//table/tr[position()>1]')
        for tr in trs:
            # find使用的是ElementPath语法
            county = tr[0].find('img').get('alt') if tr[0].find('img') is not None else None
            ip = tr[1].text
            port = tr[2].text
            adress = tr[3].find('a').text if tr[3].find('a') is not None else None
            is_anonymous = tr[4].text
            type = tr[5].text
            speed = tr[6].find('div').get('title')
            connect_time = tr[7].find('div').get('title')
            live_time = tr[8].text
            valid_time = tr[9].text
            print(county)
            print(ip)
            print(port)
            print(adress)
            print(is_anonymous)
            print(type)
            print(speed)
            print(connect_time)
            print(live_time)
            print(valid_time)


if __name__ == '__main__':
    proxy = GetProxy()
    tree = proxy.get_tree(1)
    proxy.get_proxy(tree)
