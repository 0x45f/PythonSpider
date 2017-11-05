from pymongo import MongoClient
import configparser

class MongoHandler:

	def __init__(self):
		self.__collection = None
		self.__con_mongo()

	# 连接mongo
	def __con_mongo(self):
		config = configparser.ConfigParser()
		config.read('config.ini')
		host = config['mongo']['host']
		port = int(config['mongo']['port'])
		username = config['mongo']['username']
		password = config['mongo']['password']
		database = config['mongo']['database']
		collection = config['mongo']['collection']
		client = MongoClient(host=host, port=port, username=username, password=password)
		self.__collection = client.get_database(database).get_collection(collection)

	# 将用户信息存入mongo
	def save_info(self, **info):
		self.__collection.save(info)


if __name__ == '__main__':
	pass