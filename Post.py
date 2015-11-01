import json, MySQLdb
from MyDB import db
from flask import request, Blueprint
from general_func import get_json, try_encode, inc_posts_for_thread, get_forum_dict, get_user_dict, \
	remove_post, dec_posts_for_thread, restore_post, get_post_list, get_post_by_id, get_thread_by_id

module = Blueprint('post', __name__, url_prefix='/db/api/post')

@module.route("/create/", methods=["POST"])
def create():
	request_body = request.json

	# Required
	date = request_body.get('date')
	thread = request_body.get('thread')
	message = request_body.get('message')
	user = request_body.get('user')
	forum = request_body.get('forum')

	# Optional
	parent = request_body.get('parent', None)
	if request_body.get('isApproved', False):
		is_approved = 1
	else:
		is_approved = 0

	if request_body.get('isHighlighted', False):
		is_highlighted = 1
	else:
		is_highlighted = 0

	if request_body.get('isEdited', False):
		is_edited = 1
	else:
		is_edited = 0

	if request_body.get('isSpam', False):
		is_spam = 1
	else:
		is_spam = 0

	if request_body.get('isDeleted', False):
		is_deleted = 1
	else:
		is_deleted = 0

	sql = """INSERT INTO Post (user, thread, forum, message, parent, date, \
		isSpam, isEdited, isDeleted, isHighlighted, isApproved) VALUES \
		(%(user)s, %(thread)s, %(forum)s, %(message)s, %(parent)s, %(date)s, \
		%(isSpam)s, %(isEdited)s, %(isDeleted)s, %(isHighlighted)s, %(isApproved)s);"""
	args = {'user': user, 'thread': thread, 'forum': forum, 'message': message, 'parent': parent, 'date': date,
			'isSpam': is_spam, 'isEdited': is_edited, 'isDeleted': is_deleted, 'isHighlighted': is_highlighted,
			'isApproved': is_approved}

	post_id = db.execute(sql, args, True)
	post = get_post_by_id(post_id)
	inc_posts_for_thread(thread)
	if not post:
		return json.dumps({"code": 1, "response": "Empty set"}, indent=4)

	return json.dumps({"code": 0, "response": post}, indent=4)

@module.route("/list/", methods=["GET"])
def list():
	return "todo"

@module.route("/remove/", methods=["POST"])
def remove():
	return "todo"

@module.route("/restore/", methods=["POST"])
def restore():
	return "todo"

@module.route("/update/", methods=["POST"])
def update():
	return  "todo"

@module.route("/vote/", methods=["POST"])
def vote():
	return "todo" 