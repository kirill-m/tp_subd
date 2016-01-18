import json
from flask import Flask, request
from Forum import module as forum
from Post import module as post
from User import module as user
from Thread import module as thread
from general_func import db



app = Flask(__name__)
app.register_blueprint(forum)
app.register_blueprint(post)
app.register_blueprint(user)
app.register_blueprint(thread)


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

