import urllib.request
import re
import urllib.error

__author__ = "wz"

class BDTB:

	def __init__(self):
		# https://tieba.baidu.com/p/3138733512?see_lz=1&pn=1
		# https://tieba.baidu.com/p/作为基础的url
		# 3138733512应该是帖子的编号
		# see_lz=1是否只看楼主 =0时可以取消只看楼主
		# pn=1是帖子的当前页数
		self.base_url = "https://tieba.baidu.com/p/"
		self.default_title = "百度贴吧"
		# 将要读取的页数
		self.page_index = 1
		# 打印的楼层的层数
		self.content_num = 1
		# 将读取的内容写如的文件
		self.file = None

	# 得到页面的html代码
	# question_num帖子的编号，see_lz是否只看楼主，pn页数
	def get_page_html(self, question_num, see_lz=1, pn=1):
		try:
			request = urllib.request.Request(self.base_url + str(question_num)
											 + "?see_lz=" + str(see_lz) + "&pn=" + str(pn))
			response = urllib.request.urlopen(request)
			return response.read().decode()
		except urllib.error.URLError as e:
			if hasattr(e, "reason"):
				print("出错辣！", e.reason)
			return None

	# 在html代码中找到帖子的标题
	def get_title(self, page_html):
		title_pattern = re.compile('''<h3.*?>(.*?)</h3>''', re.S)
		result = re.search(title_pattern, page_html)
		if result:
			return result.group(1)
		return None

	# 在html代码中提取帖子的总页数
	def get_page_num(self, page_html):
		page_num_pattern = re.compile('''回复贴，共.*?>(.*?)<''', re.S)
		result = re.search(page_num_pattern, page_html)
		if result:
			return int(result.group(1))
		return None

	# 从html代码中提取每层楼的内容
	def get_str_contents(self, page_html):
		contents_pattern = re.compile('''d_post_content j_d_post_content ">(.*?)</div>''', re.S)
		result = re.finditer(contents_pattern, page_html)
		if result:
			str_contents = self.replace(result)
			return str_contents
		return None

	# 替换掉无关的字符串
	def replace(self, result):
		str_contents = []
		for content in result:
			item = re.sub('''<img.*?>|<br>''', "\n", content.group(1))
			item = re.sub('''<a href.*?>|</a>| {4,7}''', "", item)
			str_contents.append(item.strip())
		return str_contents

	# 打开txt文件
	def open_file(self, title):
		if title:
			self.file = open(title + ".txt", "w+", encoding="utf-8")
		else:
			self.file = open(self.default_title + "w+", encoding="utf-8")

	# 写入文件
	def write_file(self, str_contents):
		for str_content in str_contents:
			self.file.write("楼数：" + str(self.page_index) + "-------------------------------\n")
			self.file.write(str_content + "\n")
			self.page_index += 1

	# 开始入口
	def start(self, question_num, see_lz=1):
		page_html = self.get_page_html(question_num, see_lz, self.page_index)
		title = self.get_title(page_html)
		page_num = self.get_page_num(page_html)
		self.open_file(title)
		for i in range(page_num):
			str_contents = self.get_str_contents(page_html)
			self.write_file(str_contents)
			self.page_index += 1
			page_html = self.get_page_html(question_num, see_lz, self.page_index)

if __name__ == "__main__":
	spider = BDTB()
	spider.start(3138733512, 1)
