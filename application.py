import json
from flask import Flask, request
from MyDB import db
from Forum import module as forum
from Post import module as post
from User import module as user
from Thread import module as thread

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
	print(request.query_string)
	return json.dumps({"code": 0, "response": {"user": 100000, "thread": 1000, "forum": 100, "post": 1000000}})

@app.before_request
def db_connect():
	db.initConnAndCursor()

@app.teardown_request
def db_disconnect(exception):
	db.closeConnection()

# if __name__ == '__main__':
# 	app.run(debug=True)