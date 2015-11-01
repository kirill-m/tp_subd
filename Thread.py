import json, MySQLdb
from MyDB import db
from flask import request, Blueprint
from general_func import get_json, get_thread_list, try_encode, get_forum_dict, get_user_dict, get_post_list, remove_post, \
	restore_post, str_to_json, get_thread_by_id, MYSQL_DUPLICATE_ENTITY_ERROR

module = Blueprint('thread', __name__, url_prefix='/db/api/thread')

@module.route("/create/", methods=["POST"])
def create():
	request_body = request.json
	
	# Required
	forum = request_body.get('forum')
	title = try_encode(request_body.get('title'))
	if request_body.get('isClosed'):
		is_closed = 1
	else:
		is_closed = 0
	user = request_body.get('user')
	date = request_body.get('date')
	message = request_body.get('message')
	slug = request_body.get('slug')

	# Optional
	if request_body.get('isDeleted', False):
		is_deleted = 1
	else:
		is_deleted = 0

	sql = """INSERT INTO Thread (forum, title, isClosed, user, date, message, slug, isDeleted) \
		VALUES (%(forum)s, %(title)s, %(isClosed)s, %(user)s, %(date)s, %(message)s, %(slug)s, %(isDeleted)s);"""
	args = {'forum': forum, 'title': title, 'isClosed': is_closed, 'user': user, 'date': date, 'message': message,
			'slug': slug, 'isDeleted': is_deleted}

	try:
		db.execute(sql, args, True)
	except MySQLdb.IntegrityError, message:
		print message[0]
	finally:
		thread_list = get_thread_list(title=title)
		if thread_list == list():
			return json.dumps({"code": 1, "response": "Empty set"}, indent=4)

		return json.dumps({"code": 0, "response": thread_list[0]}, indent=4)

@module.route("/list/", methods=["GET"])
def list():
	return "todo"

@module.route("/details/", methods=["GET"])
def details():
	qs = get_json(request)

	thread_id = qs.get('thread')
	if not thread_id:
		return json.dumps({"code": 2, "response": "No 'thread' key"}, indent=4)

	thread = get_thread_by_id(thread_id)
	if thread == list():
		return json.dumps({"code": 1, "response": "Empty set"}, indent=4)

	related_values = list()
	qs_related = qs.get('related')
	if type(qs_related) is list:
		related_values.extend(qs_related)
	elif type(qs_related) is str:
		related_values.append(qs_related)

	forum_related = False
	user_related = False
	for related_value in related_values:
		if related_value == 'forum':
			forum_related = True
		elif related_value == 'user':
			user_related = True
		else:
			return json.dumps({"code": 3, "response": "Wrong related value"}, indent=4)

	if forum_related:
		thread['forum'] = get_forum_dict(short_name=thread['forum'])

	if user_related:
		thread['user'] = get_user_dict(thread['user'])

	return json.dumps({"code": 0, "response": thread}, indent=4)

@module.route("/remove/", methods=["POST"])
def remove():
	return "todo"

@module.route("/open/", methods=["POST"])
def open():
	return  "todo"

@module.route("/close/", methods=["POST"])
def close():
	return "todo"

@module.route("/listPosts/", methods=["GET"])
def listPosts():
	return "todo"

@module.route("/update/", methods=["POST"])
def update():
	return "todo"

@module.route("/subscribe/", methods=["POST"])
def subscribe():
	return "todo"

@module.route("/unsubscribe/", methods=["POST"])
def unsubscribe():
	return "todo"

@module.route("/vote/", methods=["POST"])
def vote():
	return "todo"