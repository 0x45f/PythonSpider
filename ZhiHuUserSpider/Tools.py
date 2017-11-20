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
        'HTTPS://218.5.215.82:34330',
        'HTTPS://49.85.13.242:32907',
        'HTTPS://123.163.163.46:808',
        'HTTPS://182.37.40.150:808',
        'HTTPS://113.120.60.99:30473',
        'HTTPS://180.122.148.102:40395',
        'HTTPS://49.64.242.229:24506',
        'HTTPS://112.114.92.152:8118',
        'HTTPS://112.114.95.189:8118',
        'HTTPS://120.76.65.209:808',
        'HTTPS://125.124.161.221:808',
        'HTTPS://221.233.62.43:808',
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
