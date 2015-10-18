import MySQLdb

HOST = 'localhost'
USER = 'root'
DATABASE = 'tp_subd'

class MyDB:
	def __init__(self):
		self.connection = None
		self.cursor = None
		self.initConnAndCursor()

	def execute(self, sql, args=(), post=False):
		self.cursor.execute(sql, args)
		
		if post:
			self.connection.commit()
			return self.cursor.lastrowid

		return self.cursor.fetchall()

	def initConnAndCursor(self):
		if not self.connection or not self.connection.open:
			self.connection = MySQLdb.connect(host=HOST, user=USER, db=DATABASE, use_unicode=1, charset='utf8')
			self.cursor = self.connection.cursor()

	def closeConnection(self):
		self.connection.close()

db = MyDB()