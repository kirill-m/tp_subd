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
		# tm = current_milli_time()

		# try:
		self.cursor.execute(sql, args)
		# except Exception as e:
		#     print "Error %d: %s" % (e.args[0], e.args[1])

		if post:
			self.connection.commit()
			# tm = current_milli_time() - tm
			# if tm > 50:
			#    print tm, " ", sql
			return self.cursor.lastrowid

		# tm = current_milli_time() - tm
		# if tm > 50:
		#    print tm, " ", sql
		return self.cursor.fetchall()

	def initConnAndCursor(self):
		if not self.connection or not self.connection.open:
			self.connection = MySQLdb.connect(host=HOST, user=USER, db=DATABASE, use_unicode=1, charset='utf8')
			self.cursor = self.connection.cursor()

	def closeConnection(self):
		self.connection.close()

db = MyDB()