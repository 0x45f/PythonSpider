import requests

class AiWenSpider:
	def __init__(self):
		# 持久会话
		self.__session = requests.Session()
		# 使用代理
		self.__session.proxies.update({'https': '171.39.29.221'})
		# http://iask.sina.com.cn/c/95-all-1-new.html
		# iask.sina.com.cn作为基础地址，/c/95-all-1-new.html部分是每一页问题的详细地址
		self.__baseURL = 'iask.sina.com.cn'

	def getHTML(self, footURl):
		response = self.__session.get(self.__baseURL + footURl)
		return response.text


if __name__ == '__main__':
	spider = AiWenSpider()
