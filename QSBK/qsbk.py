import urllib.request
import urllib.error
import re

__author__ = "wz"

class QSBK:
	def __init__(self):
		# 表示下一次要读取的页面
		self.index = 1
		self.header = {
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36"
		}
		self.url = "https://www.qiushibaike.com/hot/page/"
		self.mainUrl = "https://www.qiushibaike.com"
		# 每个元素存储一页提取好的段子
		self.stories = []
		# enable = True 时获取下一页的段子
		self.enable = False

	# 获得页面内容
	def getPage(self, index=None, contentUrl=None):
		try:
			response = None
			if index:
				request = urllib.request.Request(self.url + str(index), headers=self.header)
				response = urllib.request.urlopen(request)
			elif contentUrl:
				request = urllib.request.Request(self.mainUrl + contentUrl, headers=self.header)
				response = urllib.request.urlopen(request)
			return response.read().decode()

		except urllib.error.URLError as e:
			print("getPage失败")
			if hasattr(e, "code"):
				print(e.code)
			if hasattr(e, "reason"):
				print(e.reason)
			return None

	# 提取每一页中不带图片的段子
	def getPageItems(self, index):
		content = self.getPage(index=index)
		# 分组信息：1发布人，2段子的全部信息的部分地址， 3发布内容， 4发布图片， 5点赞数
		pattern = re.compile('''<div class="article.*?<h2>(.*?)</h2>'''
							 + '''.*?<a href="(.*?)"'''
							 + '''.*?<span>(.*?)</span>'''
							 + '''.*?<!-- 图片或gif -->(.*?)<div class="stats">'''
							 + '''.*?<span class="stats-vote"><i class="number">(.*?)</i>''', re.S)
		items = re.finditer(pattern, content)
		pageItems = []
		# 一个item代表一个段子
		for item in items:
			# 如果段子中没有图片，保存段子
			if not re.search("img", item.group(4)):
				# 如果已经显示了段子的全部内容
				# print(item.group())
				if not re.search("查看全文", item.group()):
					result = re.sub("<br/>", "\n", item.group(3))
					pageItems.append([item.group(1).strip(), result.strip(), item.group(5).strip()])
				# 没有显示全部内容，通过item[1]发起请求访问段子的全部内容
				else:
					contentForAll = self.getPage(contentUrl=item.group(2))
					# ForAll页面的正则表达式是之前的不太相同
					patternForAll = re.compile('''<div class="article.*?<h2>(.*?)</h2>'''
											   + '''.*?<div class="content">(.*?)</div>'''
											   + '''.*?<span class="stats-vote"><i class="number">(.*?)</i>''', re.S)
					itemForAll = re.findall(patternForAll, contentForAll)
					result = re.sub("<br/>", "\n", itemForAll[0][1])
					pageItems.append([itemForAll[0][0].strip(), result.strip(), itemForAll[0][2].strip()])
		return pageItems

	# 加载并提取页面的内容，加入到列表中
	def loadPage(self):
		if self.enable:
			# 如果当前未看的页数少于2页，则加载新一页
			if len(self.stories) < 2:
				pageStories = self.getPageItems(self.index)
				if pageStories:
					self.stories.append(pageStories)
					self.index += 1

	# 获取一个段子
	def getOneStory(self, pageStories, page):
		for story in pageStories:
			# python3之后raw_input已经被抛弃
			receive = input()
			self.loadPage()

			if receive == "Q" or receive == "q":
				self.enable = False
				return
			print("当前第:%s页\n发布人:%s\n内容:%s\n点赞数:%s\n" % (page, story[0], story[1], story[2]))

	# 开始
	def start(self):
		self.enable = True
		self.loadPage()
		nowPage = 0
		while self.enable:
			if len(self.stories) > 0:
				pageStories = self.stories[0]
				nowPage += 1
				del self.stories[0]
				self.getOneStory(pageStories, nowPage)


if __name__ == "__main__":
	spider = QSBK()
	spider.start()
