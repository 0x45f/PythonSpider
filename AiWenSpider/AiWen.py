import requests
from lxml import html


class AiWenSpider:

	def __init__(self):
		# 要抓取多少页
		self.__pages = 10
		# 当前页数
		self.__currentPage = 1
		# 持久会话
		self.__session = requests.Session()
		# 使用代理
		self.__session.proxies.update({'https': '171.39.29.221'})
		# http://iask.sina.com.cn/c/95-all-1-new.html
		# iask.sina.com.cn作为基础地址，/c/95-all-1-new.html部分是每一页问题的详细地址
		self.__baseURL = 'http://iask.sina.com.cn'
		self.__nextFootURL = '/c/95-all-1-new.html'

	def getTree(self, NextFootURl):
		response = self.__session.get(self.__baseURL + NextFootURl, timeout=5)
		return html.fromstring(response.text)

	def getNextFootURL(self, tree):
		result = tree.xpath('//div[@class="page mt30"]/a[@class="current"]/following::a[2]')
		return result[0].get('href')

	def getQusFootURL(self, tree):
		result = tree.xpath('//div[@class="question-title"]')
		list = []
		for i in result:
			list.append(i[i].get('href'))
		return list


	def start(self):
		for self.__currentPage in range(self.__pages):
			tree = self.getTree(self.__nextFootURL)
			# 找到下一页的url
			self.__nextFootURL = self.getNextFootURL(tree)

if __name__ == '__main__':
	spider = AiWenSpider()
	spider.start()
