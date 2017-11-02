import pymysql
import configparser


class MySqlHandler:

	def __init__(self):
		self.__config = None
		self.__mysql_con = None
		self.__con__mysql()

	def __con__mysql(self):
		self.__config = configparser.ConfigParser()
		self.__config.read('config.ini')
		host = self.__config['mysql']['host']
		port = self.__config['mysql']['port']
		user = self.__config['mysql']['user']
		password = self.__config['mysql']['password']
		database = self.__config['mysql']['database']
		charset = self.__config['mysql']['charset']

		self.__mysql_con = pymysql.Connect(host=host, port=port, user=user, password=password,
										   database=database, charset=charset)
