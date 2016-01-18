import json
from flask import Flask, request
from MyDB import db
from Forum import module as forum
from Post import module as post
from User import module as user
from Thread import module as thread
import MySQLdb

app = Flask(__name__)
app.register_blueprint(forum)
app.register_blueprint(post)
app.register_blueprint(user)
app.register_blueprint(thread)

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

@app.route('/db/api/clear/', methods=["POST"])
def clear():
	db.execute("""DELETE Forum.* FROM Forum;""", post=True)
	db.execute("""DELETE User.* FROM User;""", post=True)
	db.execute("""DELETE Post.* FROM  Post;""")
	db.execute("""DELETE Thread.* FROM  Thread;""", post=True)
	db.execute("""DELETE Subscription.* FROM Subscription;""", post=True)
	db.execute("""DELETE Follower.* FROM Follower;""", post=True)
	return json.dumps({"code": 0, "response": "OK"})

@app.route('/db/api/status/', methods=["GET"])
def status():
	user_count = db.execute("""SELECT count(*) FROM User;""")
	thread_count = db.execute("""SELECT count(*) FROM Thread;""")
	forum_count = db.execute("""SELECT count(*) FROM Forum;""")
	post_count = db.execute("""SELECT count(*) FROM Post;""")
	
	users = user_count[0][0]
	threads = thread_count[0][0]
	forums = forum_count[0][0]
	posts = post_count[0][0]
	
	return json.dumps({"code": 0, "response": {"user": users, "thread": threads, "forum": forums, "post": posts}})

@app.before_request
def db_connect():
	db.initConnAndCursor()

