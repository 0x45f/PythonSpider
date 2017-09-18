import os
import urllib.request
import urllib.error
import urllib.parse
import json
import re


class MMSpider:

	def __init__(self):
		self.__code_type = "gbk"
		self.__http = "http:"
		self.__url = "http://mm.taobao.com/tstar/search/tstar_model.do?_input_charset=utf-8"
		# 每个模特主页的地址
		self.__base_person_url = "http://mm.taobao.com/self/aiShow.htm?userId="
		# 相册的地址
		self.__base_all_album_url = "https://mm.taobao.com/self/album/open_album_list.htm?_charset=utf-8&user_id%20="
		# 具体相册地址
		self.__base_pic_url = "https://mm.taobao.com/album/json/get_album_photo_list.htm?user_id="

		# r表示python的原生字符串 每个模特创建一个文件夹，表示存储的地址
		self.__base_path = r"F:\TaoBaoMM"
		# 想要提取的页数
		self.__total_page = 1
		# 当前正在提取的页数
		self.__currentPage = 1
		# 找到具体album的id的正则表达式
		self.__album_pattern = re.compile('''<h4>.*?album_id=(.*?)&''', re.S)
		# album有多少的的正则表达式
		self.__album_page_pattern = re.compile('''<input name="totalPage" id="J_Totalpage" value="(.*?)"''', re.S)

	# 由页面返回的json数据得到字典,会得到30个模特的具体信息
	def get_person_dict(self, currentPage):
		try:
			data = urllib.parse.urlencode({"currentPage": currentPage}).encode("utf-8")
			request = urllib.request.Request(self.__url, data=data)
			response = urllib.request.urlopen(request)
			result = response.read().decode(self.__code_type)
			return json.loads(result)
		except urllib.error.URLError as e:
			print("出错了！", e.reason)

	# 保存信息MM的文字图片信息
	def save(self, searchDOList):
		# 进入每个模特的主页，找到相册地址
		# 保存对每个模特创建一个文件夹，保存文字信息并进入相册下载图片
		for person in searchDOList:
			# 创建文件夹，保持信息
			dir_path = self.__base_path + "\\" + person["realName"]
			if self.mkdir(dir_path):
				# 模特个人主页的url
				txt_path = dir_path + "\\" + person["realName"] + ".txt"
				self.write_txt(txt_path, person)
				self.save_imgs(person, dir_path)


	# 每个MM保存1000张照片 每个人照片实在太多了
	def save_imgs(self, person, dir_path):
		# 找到MM的相册一共有多少页
		album_page = self.get_album_page(person["userId"])
		img_index = 1
		# 在每一页中操作找到该页中album的id
		for i in range(1, int(album_page) + 1):
			album_ids = self.get_album_ids(person["userId"], i)
			for album_id in album_ids:
				pic_page = self.get_pic_page(person["userId"], album_id)
				# 将每一个中的图片的地址保存下来
				for j in range(1, int(pic_page) + 1):
					imgs_url = self.get_imgs_url(person, j, album_id)
					for img_url in imgs_url:
						try:
							url = self.__http + img_url["picUrl"]
							response = urllib.request.urlopen(url, timeout=5)
							with open(dir_path + "\\" + str(img_index) + ".jpg", "wb") as file:
								file.write(response.read())
								# 好像写成了保存999张
								img_index = img_index + 1
								if img_index >= 1000:
									print(person["realName"] + ":已经保存1000张辣")
									return
						except TimeoutError as e:
							print(e.strerror)
						except urllib.error.URLError as e:
							print(e.reason)
						except BaseException as e:
							print(e.args)

	# 创建新的文件夹
	def mkdir(self, dir_path):
		if os.path.exists(dir_path):
			return False
		# 文件夹不存在时才创建
		else:
			os.mkdir(dir_path)
			return True

	# 新建txt文件并将文字信息写入txt文件
	def write_txt(self, txt_path, person):
		person_url = self.__base_person_url + str(person["userId"])
		content = "姓名：" + person["realName"] + "  城市：" + person["city"] \
				  + "\n身高：" + str(person["height"]) + "  体重：" + str(person["weight"]) \
				  + "\n喜欢：" + str(person["totalFavorNum"]) \
				  + "\n个人主页：" + person_url
		with open(txt_path, "w", encoding="utf-8") as file:
			print(person["realName"] + ":正在保存" + person["realName"] + "的文字信息")
			file.write(content)

	# 保存图片的地址
	def get_imgs_url(self, person, j, album_id):
		url = self.__base_pic_url + str(person["userId"]) \
			  + "&album_id=" + str(album_id) \
			  + "&page=" + str(j)
		try:
			response = urllib.request.urlopen(url, timeout=5)
			result = response.read().decode(self.__code_type)
			imgs_url = json.loads(result)["picList"]
			return imgs_url
		except TimeoutError as e:
			print(e.strerror)
		except urllib.error.URLError as e:
			print(e.reason)
		except BaseException as e:
			print(e.args)

	# 由第page页找到该页中所有album的id
	def get_album_ids(self, userId, page):
		try:
			all_album_url = self.__base_all_album_url + str(userId) + "&" + str(page)
			request = urllib.request.Request(all_album_url)
			response = urllib.request.urlopen(request)
			html = response.read().decode(self.__code_type)
			# 提取该页中album的id
			return re.findall(self.__album_pattern, html)
		except urllib.error.URLError as e:
			print("提取相册id出错了！", e.reason)

	# 找到一个相册内的图片有多少页
	def get_pic_page(self, userId, albumId):
		try:
			# 先得到这个相册一共有多少页
			url = self.__base_pic_url + str(userId) + "&album_id=" + str(albumId)
			response = urllib.request.urlopen(url)
			result = json.loads(response.read().decode(self.__code_type))
			return result["totalPage"]
		except urllib.error.URLError as e:
			print(e.reason)
			return None

	# 得到MM一共有多少页的相册
	def get_album_page(self, userId):
		try:
			all_album_url = self.__base_all_album_url + str(userId)
			response = urllib.request.urlopen(all_album_url)
			html = response.read().decode(self.__code_type)
			return re.search(self.__album_page_pattern, html).group(1)
		except urllib.error.URLError as e:
			print("得到MM一共有多少页的相册出错啦", e.reason)
		return None

	def start(self):
		print("开始辣！")
		for i in range(self.__total_page):
			dict_result = self.get_person_dict(self.__currentPage)
			searchDOList = dict_result["data"]["searchDOList"]
			# 保存所有本页中MM的信息
			self.save(searchDOList)
			self.__currentPage += 1
if __name__ == "__main__":
	spider = MMSpider()
	spider.start()
