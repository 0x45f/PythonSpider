import redis
import configparser


class RedisHandler:

	def __init__(self):
		self.__config = None
		self.__redis_con = None
		self.__hash_name = None
		self.__list_name = None
		self.__con_redis()

	# 连接redis数据库
	def __con_redis(self):
		self.__config = configparser.ConfigParser()
		self.__config.read('config.ini')
		host = self.__config['redis']['host']
		port = self.__config['redis']['port']
		password = self.__config['redis']['password']
		self.__hash_name = self.__config['redis']['hash_name']
		self.__list_name = self.__config['redis']['list_name']

		# print(port)
		self.__redis_con = redis.Redis(host=host, port=port, password=password)
		# self.__redis_con.hset('onehash', '123', '123')

	# 将已经存储了的用户存入hash中
	def save_url_token(self, *url_token):
		for i in url_token:
			self.__redis_con.hset(self.__hash_name, i, 1)
