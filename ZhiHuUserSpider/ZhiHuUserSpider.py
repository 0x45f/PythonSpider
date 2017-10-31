import requests
from lxml import html
import json


class ZhiHuUserSpoder:

	def __init__(self):
		self.__base_url = 'https://www.zhihu.com'
		self.__headers = {
			'accept': 'application / json, text / plain, * / *',
			'Accept - Encoding': 'gzip, deflate, br',
			'Accept - Language': 'zh - CN, zh;q = 0.8',
			'authorization': 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20',
			'Host': 'www.zhihu.com',
			'Referer': 'https://www.zhihu.com/',
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
						  'Chrome/61.0.3163.100 Safari/537.36 ',
			'X - UDID': 'AFDC3cbZvguPTk1xbYYtpQt214bsP2px88I ='
		}
		self.__session = requests.session()
		# 字典的update方法进行并集更新
		self.__session.headers.update(self.__headers)
		self.__session.proxies.update({'HTTP': 'HTTP://49.81.254.120:8118'})

	def get_tree(self, url):
		text = self.__session.get(url).text
		# print(html.fromstring(text).__class__)
		return html.fromstring(text)

	# 获取首页上出现的用户的主页地址
	def get_users_url_from_index(self):
		tree = self.get_tree(self.__base_url + '/explore')
		users_url = tree.xpath('//a[@class="author-link"]/@href')
		# for url in users_url:
		# 	print(url)
		return users_url

	# 获取某个用户关注的人的主页地址
	def get_following(self, url_token):
		url = self.__base_url + '/api/v4/members/' \
			  + url_token + '/followees?include=data%5B*%5D.answer_count' \
							'%2Carticles_count%2Cgender%2Cfollower_count' \
							'%2Cis_followed%2Cis_following%2Cbadge%5B%3F(' \
							'type%3Dbest_answerer)%5D.topics&offset=0&limit=20'
		# dump和dumps是将python对象转换成json格式；load和loads是将json格式转换成python对象
		text = self.__session.get(url).text
		res = json.loads(text)

	# 获取关注该用户的人的主页地址
	def get_followers(self, url):
		pass

if __name__ == '__main__':
	spider = ZhiHuUserSpoder()
	spider.get_following('xie-jia-tong-35')


