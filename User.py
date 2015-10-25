import json, MySQLdb
from MyDB import db
from flask import request, Blueprint
from general_func import try_encode, MYSQL_DUPLICATE_ENTITY_ERROR, get_user_dict

module = Blueprint('user', __name__, url_prefix='/db/api/user')

@module.route("/create/", methods=["POST"])
def create():
	request_body = request.json

	username = try_encode(request_body.get('username'))
	about = request_body.get('about')
	name = try_encode(request_body.get('name'))
	email = request_body.get('email')
	is_anonymous_key = request_body.get('isAnonymous', False)
	if is_anonymous_key:
		is_anonymous = 1
	else:
		is_anonymous = 0

	sql = """INSERT INTO User (username, about, name, email, isAnonymous) VALUES \
		(%(username)s, %(about)s, %(name)s, %(email)s, %(isAnonymous)s);"""
	args = {'username': username, 'about': about, 'name': name, 'email': email, 'isAnonymous': is_anonymous}

	try:
		db.execute(sql, args, True)
	except MySQLdb.IntegrityError, message:
		if message[0] == MYSQL_DUPLICATE_ENTITY_ERROR:
			return json.dumps({"code": 5,
							   "response": "This user already exists"}, indent=4)
		return json.dumps({"code": 4,
						   "response": "Oh, we have some really bad error"}, indent=4)

	user_dict = get_user_dict(email)

	return json.dumps({"code": 0, "response": user_dict}, indent=4)

@module.route("/details/", methods=["GET"])
def details():
	return "todo"

@module.route("/follow/", methods=["POST"])
def follow():
	return "todo"

@module.route("/unfollow/", methods=["POST"])
def unfollow():
	return  "todo"

@module.route("/listPosts/", methods=["GET"])
def listPosts():
	return "todo"

@module.route("/updateProfile/", methods=["POST"])
def updateProfile():
	return "todo"

@module.route("/listFollowers/", methods=["GET"])
def listFollowers():
	return "todo"

@module.route("/listFollowing/", methods=["GET"])
def listFollowing():
	return "todo"   