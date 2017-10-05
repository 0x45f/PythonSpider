import requests
from lxml import html


class AiWenSpider:

	def __init__(self):
		# 要抓取多少页
		self.__pages = 1
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

	# 得到下一页尾部的url
	def getNextFootURL(self, tree):
		result = tree.xpath('//div[@class="page mt30"]/a[@class="current"]/following::a[2]')
		return result[0].get('href')

	# 得到本页中所有问题的尾部url
	def getQusFootURL(self, tree):
		result = tree.xpath('//div[@class="question-title"]/a')
		qusURLList = []
		for i in result:
			qusURLList.append(i.get('href'))
		return qusURLList

	# 得到问题的内容
	def getQusContent(self, tree):
		qusId = tree.xpath('//div[@id="paramDiv"]/@questionid')[0]
		title = tree.xpath('//div[@class="question_text"]/pre')[0].text
		goodAns = tree.xpath('//div[@class="good_answer"]//pre')[0].text
		otherAns = tree.xpath('//div[@class="answer_list"]//pre')
		ansList = []
		for ans in otherAns:
			ansList.append(ans.text)
		return {
			'qusId': qusId,  # 问题id
			'title': title,  # 问题的标题
			'goodAns': goodAns,  # 最佳答案
			'ansList': ansList  # 其他答案的列表
		}


	def start(self):
		for self.__currentPage in range(self.__pages):
			tree = self.getTree(self.__nextFootURL)
			# 找到下一页的url
			self.__nextFootURL = self.getNextFootURL(tree)
			# 找到本页中所有问题的url
			qusURLList = self.getQusFootURL(tree)
			for qusURL in qusURLList:
				qusTree = self.getTree(qusURL)
				content = self.getQusContent(qusTree)

if __name__ == '__main__':
	spider = AiWenSpider()
	spider.start()
