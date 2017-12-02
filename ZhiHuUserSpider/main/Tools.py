import random
import logging

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
        'HTTPS://112.114.97.25:8118',
        'HTTPS://171.39.116.232:8123',
        'HTTPS://110.73.54.191:8123',
        'HTTPS://113.121.42.47:808',
        'HTTPS://118.72.124.97:80',
        'HTTPS://110.73.43.162:8123',
        'HTTPS://112.114.93.186:8118',
        'HTTPS://106.58.152.75:80',
        'HTTPS://60.210.104.254:808',
        'HTTPS://171.36.176.249:8118',
        'HTTPS://112.114.95.179:8118',
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
    logging.error(123)
