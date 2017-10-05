import pymysql


class DBHelper:
	def __init__(self):
		# 链接数据库
		pass

	def insert(self):
		# 插入一条数据
		pass


if __name__ == "__main__":
	# charset 默认是 latin1, 查询到中文会是？？
	conn = pymysql.connect(host='localhost', user='root', password='123', database='test', charset='utf8')
	cur = conn.cursor()
	cur.execute("select * from linkman")
	data = cur.fetchall()
	for i in data:
		print(i[0])

