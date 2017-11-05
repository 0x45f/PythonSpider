import redis
import configparser


class RedisHandler:

	def __init__(self):
		self.__redis_con = None
		self.__hash_name = None
		self.__list_name = None
		self.__con_redis()

	# 连接redis数据库
	def __con_redis(self):
		config = configparser.ConfigParser()
		config.read('config.ini')
		host = config['redis']['host']
		port = config['redis']['port']
		password = config['redis']['password']
		self.__hash_name = config['redis']['hash_name']
		self.__list_name = config['redis']['list_name']

		# print(port)
		self.__redis_con = redis.Redis(host=host, port=port, password=password)
		# self.__redis_con.hset('onehash', '123', '123')

	# # 将已经存储了的用户存入hash中
	# def save_url_token(self, *url_token):
	# 	for i in url_token:
	# 		if self.__redis_con.hexists(self.__hash_name, i):
	# 			self.__redis_con.hset(self.__hash_name, i, 1)

	# 将还未爬取的url_token加入list尾部，同时加入到hash中
	def save_url_token(self, url_token):
		if not self.__redis_con.hexists(self.__hash_name, url_token):
			self.__redis_con.hset(self.__hash_name, url_token, 1)
			self.__redis_con.rpush(self.__list_name, url_token)

	# 从redis的list头部返回一个没有爬取的url,blpop：如果list未空则阻塞
	def get_url_token(self):
		return self.__redis_con.lpop(self.__list_name)

	# 获得list长度
	def get_list_len(self):
		return self.__redis_con.llen(self.__list_name)
