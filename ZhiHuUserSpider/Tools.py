import telnetlib
import random


class Tools:

    ua = (
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36 OPR/37.0.2178.32',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586'
    )
    proxies = (
        'HTTPS://116.54.250.210:4370',
        'HTTPS://218.88.215.109:8118',
        'HTTPS://182.110.228.231:4323',
        'HTTPS://114.230.30.68:808',
        'HTTPS://221.198.105.220:8118',
        'HTTPS://120.76.55.49:8088'
    )
    proxy_count = -1

    @classmethod
    def get_ua(cls):
        return cls.ua[random.randint(0, len(cls.ua) - 1)]

    @classmethod
    def get_proxy(cls):
        cls.proxy_count += 1
        return cls.proxies[cls.proxy_count % len(cls.proxies)]

if __name__ == '__main__':
    tools = Tools()
    print(tools.get_ua())
    print(tools.get_proxy)
