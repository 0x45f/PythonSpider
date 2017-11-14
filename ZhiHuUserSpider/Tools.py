import telnetlib
import random

class Tools:

	def __init__(self):
		self.__ua = (
			'User-Agent, Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)',
			'User-Agent, Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)',
			'User-Agent,Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)',
			'User-Agent,Mozilla/5.0 (Windows NT 6.1; rv,2.0.1) Gecko/20100101 Firefox/4.0.1',
			'User-Agent, MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1'
		)
		self.__proxies = (
			'HTTPS://116.54.250.210:4370',
			'HTTPS://218.88.215.109:8118',
			'HTTPS://182.110.228.231:4323',
			'HTTPS://114.230.30.68:808',
			'HTTPS://221.198.105.220:8118',
			'HTTPS://120.76.55.49:8088'
		)

	def get_ua(self):
		return self.__ua[random.randint(0, len(self.__ua)-1)]

	def get_proxy(self):
		return self.__proxies[random.randint(0, len(self.__proxies)-1)]

if __name__ == '__main__':
	tools = Tools()
	print(tools.get_ua())
	print(tools.get_proxy())


