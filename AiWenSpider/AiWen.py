import requests
from lxml import html
import DB
import time
import re


class AiWenSpider:

	def __init__(self):
		# 初始化数据库
		self.__db = DB.DBHelper()
		# 要抓取多少页
		self.__pages = 50
		# 当前页数
		self.__currentPage = 0
		# 持久会话
		self.__session = requests.Session()
		# 使用代理
		self.__session.proxies.update({'https': '171.39.29.221'})
		# http://iask.sina.com.cn/c/95-goodAnswer-1-new.html 是已经解答问题的分类
		# iask.sina.com.cn作为基础地址，/c/95-goodAnswer-1-new.html部分是每一页问题的详细地址
		self.__baseURL = 'http://iask.sina.com.cn'
		self.__nextFootURL = '/c/95-goodAnswer-1-new.html'
		self.__QUSTABLE = 'iask_questions'
		self.__ANSTABLE = 'iask_answers'

	def getTree(self, NextFootURl):
		response = self.__session.get(self.__baseURL + NextFootURl, timeout=5)
		return html.fromstring(response.text)

	# 得到下一页尾部的url
	def getNextFootURL(self, tree):
		result = tree.xpath('//div[@class="page mt30"]/a[@class="current"]/following::a[@href]')
		return result[0].get('href')

	# 得到本页中所有问题的尾部url
	def getQusFootURL(self, tree):
		result = tree.xpath('//div[@class="question-title"]/a')
		qusURLList = []
		for i in result:
			qusURLList.append(i.get('href'))
		return qusURLList

	# 保存问题
	# 保存id，问题内容，提问者，提问时间，回答数量，问题链接
	def saveQus(self, tree):
		questionId = tree.xpath('//input[@id="questionId"]/@value')[0]
		qcontent = tree.xpath('//div[@id="paramDiv"]/@qcontent')[0]
		# 匿名提问和实名提问不同
		try:
			# 实名提问
			qusAuthor = tree.xpath('//div[@class="ask_autho cf"]/span[@class="user_wrap"]/a')[0].text
		except IndexError:
			# 匿名提问
			qusAuthor = tree.xpath('//div[@class="ask_autho cf"]/span[@class="gary gray-a"]')[0].text
		postDate = tree.xpath('//input[@id="postDate"]/@value')[0]
		lengood = int(tree.xpath('//div[@id="paramDiv"]/@lengood')[0])
		lenother = int(tree.xpath('//div[@id="paramDiv"]/@lenother')[0])
		ansCount = lengood + lenother
		url = tree.xpath('//link[@rel="canonical"]/@href')[0]
		myDict = {
			'questionId': questionId,
			'qcontent': qcontent,
			'qusAuthor': qusAuthor,
			'postDate': postDate,
			'ansCount': ansCount,
			'url': url
		}
		# 将字典插入数据库
		self.__db.insert(self.__QUSTABLE, myDict)
		return lengood

	# 保存好评回答
	# 保存id，回答内容，问题id，回答者，回答时间，是否是最佳答案:1好评答案，0其他答案
	def saveGoodAns(self, tree):
		# html代码中这个qId属性应该是回答的唯一标识
		qId = tree.xpath('//div[@class="good_answer"]//span[@class="praise mr15"]/@qid')[0]
		ansContent = tree.xpath('//div[@class="good_answer"]/div[@class="answer_text"]//pre')[0].text
		ansContent = self.replace(ansContent)
		questionId = tree.xpath('//input[@id="questionId"]/@value')[0]
		ansAuthor = tree.xpath('//div[@class="good_answer"]//a[@class="blue408"]')[0].text
		postDate = tree.xpath('//div[@class="good_answer"]//span[@class="time mr10"]')[0].text
		isGood = 1
		myDict = {
			'qId': qId,
			'ansContent': ansContent,
			'questionId': questionId,
			'ansAuthor': ansAuthor,
			'postDate': postDate,
			'isGood': isGood
		}
		# 存入数据库
		self.__db.insert(self.__ANSTABLE, myDict)

	# 保存其他回答
	# 保存id，回答内容，问题id，回答者，回答时间，是否是最佳答案
	def saveOtherAns(self, tree):
		# 找到问题id
		questionId = tree.xpath('//input[@id="questionId"]/@value')[0]
		for i in tree.xpath('//div[@class="answer-info"]'):
			# The ElementTree library comes with a simple XPath-like path language called ElementPath.
			qId = i.find('.//span[@class="praise mr15"]').get('qid')
			ansContent = i.findtext('.//pre')
			ansContent = self.replace(ansContent)
			ansAuthor = i.findtext('.//a[@class="author_name"]')
			postDate = i.findtext('.//span[@class="answer_t"]')
			isGood = 0
			myDict = {
				'qId': qId,
				'ansContent': ansContent,
				'questionId': questionId,
				'ansAuthor': ansAuthor,
				'postDate': postDate,
				'isGood': isGood
			}
			# 将字典存入数据库
			self.__db.insert(self.__ANSTABLE, myDict)

	def replace(self, content):
		# TypeError: expected string or bytes-like object
		# str()保证content是str
		content = re.sub('"', '', str(content))
		return content

	def start(self):
		for self.__currentPage in range(self.__pages):
			print('开始保存%s....' % (self.__baseURL + self.__nextFootURL))
			tree = self.getTree(self.__nextFootURL)
			# 找到下一页的url
			self.__nextFootURL = self.getNextFootURL(tree)
			# 找到本页中所有问题的url
			qusURLList = self.getQusFootURL(tree)
			for qusURL in qusURLList:
				qusTree = self.getTree(qusURL)
				# 特意找了已解决问题但是还是会有没有最佳答案的问题。
				lengood = self.saveQus(qusTree)
				if lengood != 0:
					self.saveGoodAns(qusTree)
				self.saveOtherAns(qusTree)
			time.sleep(1)
		print('保存完成')

if __name__ == '__main__':
	spider = AiWenSpider()
	spider.start()
