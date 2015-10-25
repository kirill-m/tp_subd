import json, MySQLdb
from MyDB import db
from flask import request, Blueprint
from general_func import get_forum_dict, get_json, get_user_dict, \
	get_subscribed_threads_list, get_post_list, get_thread_list, str_to_json, get_thread_by_id

module = Blueprint('forum', __name__, url_prefix='/db/api/forum')

@module.route("/create/", methods=["POST"])
def create():
	request_body = request.json

	name = request_body.get('name')
	short_name = request_body.get('short_name')
	user = request_body.get('user')

	try:
		db.execute("""INSERT INTO Forum (name, short_name, user) VALUES (%(name)s, %(short_name)s, %(user)s);""",
				   {'name': name, 'short_name': short_name, 'user': user}, True)
	except MySQLdb.IntegrityError, message:
		print message[0]
	finally:
		forum_dict = get_forum_dict(short_name=short_name)
		return json.dumps({"code": 0, "response": forum_dict}, indent=4)

@module.route("/details/", methods=["GET"])
def details():
	qs = get_json(request)
	short_name = qs.get('forum')

	if not short_name:
		return json.dumps({"code": 2, "response": "No 'forum' key"}, indent=4)

	forum_dict = get_forum_dict(short_name=short_name)
	if not forum_dict:
		return json.dumps({"code": 1, "response": "Empty set"}, indent=4)

	if qs.get('related', '') == 'user':
		forum_dict['user'] = get_user_dict(forum_dict['user'])

	return json.dumps({"code": 0, "response": forum_dict}, indent=4)

@module.route("/listPosts/", methods=["GET"])
def listPosts():
	return  "todo"

@module.route("/listThread/", methods=["GET"])
def listThread():
	return "todo"

@module.route("/listUsers/", methods=["GET"])
def listUsers():
	return "todo"

		   