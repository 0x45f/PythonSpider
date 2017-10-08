import pymysql


class DBHelper:
	def __init__(self):
		# 链接数据库
		try:
			# charset 默认是 latin1, 查询到中文会是？？
			# charset='utf8mb4' 避免有表情时插入错误
			self.__db = pymysql.connect(host='localhost', user='root', password='123', database='test', charset='utf8mb4')
			self.__cur = self.__db.cursor()
		except pymysql.Error as e:
			print('链接数据库失败：', e.args[0], e.args[1])

	def insert(self, table, myDict):
		# 答案中存在表情会出错
		# 答案中存在双引号会出错，sql语句会发生歧义
		# 插入一条数据
		try:
			cols = ','.join(myDict.keys())
			values = ','.join(map(lambda x: '"'+str(x)+'"', myDict.values()))
			sql = 'INSERT INTO %s (%s) VALUES (%s)' % (table, cols, values)
			result = self.__cur.execute(sql)
			self.__db.commit()
			# if result:
			# 	print('保存成功！')
			# else:
			# 	print('保存失败！')
		except pymysql.Error as e:
			print('插入失败：', e.args[0], e.args[1])
			# 发生错误时回滚
			self.__db.rollback()

