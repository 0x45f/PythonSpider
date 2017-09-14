2017/9/10 22:25:28  

博主地址http://cuiqingcai.com/990.html

博主源代码

    # -*- coding:utf-8 -*-
    import urllib
    import urllib2
    
    
    page = 1
    url = 'http://www.qiushibaike.com/hot/page/' + str(page)
    try:
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        print response.read()
    except urllib2.URLError, e:
        if hasattr(e,"code"):
        print e.code
        if hasattr(e,"reason"):
        print e.reason

遇到问题**http.client.RemoteDisconnected: Remote end closed connection without response**

利用 urllib 发起的请求，UA 默认是 Python-urllib/3.5 而在 chrome 中访问 UA 则是 User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36，因为服务器根据 UA 来判断拒绝了 python 爬虫。
在request中加入header应该就可以了.python版本是3.5

更改后的代码如下：

    import urllib.request
    import urllib.error
    
    __author__ = "wz"
    
    page = 1
    url = "http://www.qiushibaike.com/hot/page/" + str(page)
    header = {
    	"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36"
    }
    try:
        	request = urllib.request.Request(url,  headers=header)
    	    response = urllib.request.urlopen(request)
        	print(response.read().decode("utf-8"))
    except urllib.error.URLError as e:
    	   if hasattr(e, "code"):
    		  print(e.code)
    	   if hasattr(e, "reason"):
    		  print(e.reason)

成功得到了response

加入正则表达式后的代码：

    __author__ = "wz"

    import urllib.request
    import urllib.error
    import re
    
    page = 1
    url = "http://www.qiushibaike.com/hot/page/" + str(page)
    header = {
    	"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36"
    }
    try:
    	request = urllib.request.Request(url, headers=header)
    	response = urllib.request.urlopen(request)
    	content = response.read().decode("utf-8")
    	pattern = re.compile('''<div class="article block untagged mb15.*?<h2>(.*?)</h2>'''
    						 + '''.*?<span>(.*?)</span>'''
    						 + '''.*?<!-- 图片或gif -->(.*?)<div class="stats">'''
    						 +'''.*?<span class="stats-vote"><i class="number">(.*?)</i>''', re.S)
    	items = re.findall(pattern, content)
    	# print("items len:", items.__len__())
    	for item in items:
    		# 0发布人，1发布内容， 2发布图片， 3点赞数
    		for i in range(4):
    			print(item[i])
    	# print(response.read().decod("utf-8"))
    except urllib.error.URLError as e:
    	if hasattr(e, "code"):
    		print(e.code)
    	if hasattr(e, "reason"):
    		print(e.reason)

测试后可以得到0发布人，1发布内容， 2发布图片， 3点赞数，改版后糗事百科是不是没有了发布时间？我咋没找到

但是打印后发现item每个元素首尾有很多空格str可以去除空格的方法 `str.lstrip([chars]) ``str.rstrip([chars]`
`str.strip([chars])`

将上面代码完善后:

    __author__ = "wz"
    
    import urllib.request
    import urllib.error
    import re
    
    
    class QSBK:
    	def __init__(self):
    		# 表示下一次要读取的页面
    		self.index = 1
    		self.header = {
    			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36"
    		}
    		self.url = "https://www.qiushibaike.com/hot/page/"
    		# 每个元素存储一页提取好的段子
    		self.stories = []
    		# enable = True 时获取下一页的段子
    		self.enable = False
    
    	# 获得下标为indxe页面的内容
    	def getPage(self, index):
    		try:
    			request = urllib.request.Request(self.url + str(index), headers=self.header)
    			respense = urllib.request.urlopen(request)
    			return respense.read().decode()
    
    		except urllib.error.URLError as e:
    			print("getPage失败")
    			if hasattr(e, "code"):
    				print(e.code)
    			if hasattr(e, "reason"):
    				print(e.reason)
    			return None
    
    	# 提取每一页中不带图片的段子
    	def getPageItems(self, index):
    		content = self.getPage(index)
    		# 0发布人，1发布内容， 2发布图片， 3点赞数
    		pattern = re.compile('''<div class="article block untagged mb15.*?<h2>(.*?)</h2>'''
    							 + '''.*?<span>(.*?)</span>'''
    							 + '''.*?<!-- 图片或gif -->(.*?)<div class="stats">'''
    							 + '''.*?<span class="stats-vote"><i class="number">(.*?)</i>''', re.S)
    		items = re.findall(pattern, content)
    		pageItems = []
    		#############################################################
    		for item in items:
    			# 如果段子中没有图片, 去除<br/>
    			if not re.search("img", item[2]):
    				result = re.sub('<br/>', "\n", item[1])
    				pageItems.append([item[0].strip(), result.strip(), item[3].strip()])
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
    			recive = input()
    			self.loadPage()
    
    			if recive == "Q" or recive == "q":
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


但是！！！！！！！！！！！！！！好像有的段子不完整啊！！！！！！！！！！！！
原来是比较长的段子有查看原文这么一个东西，改变一下代码获取完整的段子：

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


### 关于.*?的惰性匹配
惰性匹配是从左开始，往右最短的匹配，而不是左右两端最短的匹配。
比如说content是`<div<div<div>` 正则表达式是`<div(.*?)>`匹配到的结果是整个字符串`<div<div<div>`而不是`<div>`

### 关于encode()和decode()
- decode是解码，它是将不是unicode的格式解码（转换）成unicode格式，使用时必须知道其格式。
- encode是编码，它是将unicode格式编码（转换）成非unicode格式，使用时必须是unicode格式。

###关于re.match()、re.search()、re.findall()和re.finditer()的区别

re.search()和re.match()函数

- re.search()和re.match()函数如果匹配成功都是仅返回**一个**match对象
- re.search 扫描整个字符串并返回第一个成功的匹配。
- match()尝试从字符串的起始位置匹配一个模式，如果不是起始位置匹配成功的话，match()就返回none。

re.findall()函数

- 当给出的正则表达式中带有多个括号且有多个匹配结果时，返回tuple的lsit。
- 当给出的正则表达式中带有一个括号时，列表的元素为字符串，此字符串的内容与括号中的正则表达式相对应（不是整个正则表达式的匹配内容）。
- 当给出的正则表达式中不带括号时，列表的元素为字符串，此字符串为整个正则表达式匹配的内容。

re.finditer()函数

-从左到右扫描的，匹配按照发现的顺序返回。
-扫描整个字符串并返回返回iterator产生match objects



#划重点！！！！！！

#第一次写python代码，贼菜，很多不好的地方请多多指教
