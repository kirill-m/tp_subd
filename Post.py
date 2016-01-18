import json, MySQLdb
from application import db
from flask import request, Blueprint
from general_func import get_json, try_encode, inc_posts_for_thread, get_forum_dict, get_user_dict, \
	remove_post, dec_posts_for_thread, restore_post, get_post_list, get_post_by_id, get_thread_by_id

module = Blueprint('post', __name__, url_prefix='/db/api/post')

@module.route("/create/", methods=["POST"])
def create():
	requestBody = request.json

	# Required
	date = requestBody.get('date')
	thread = requestBody.get('thread')
	message = requestBody.get('message')
	user = requestBody.get('user')
	forum = requestBody.get('forum')

	# Optional
	parent = requestBody.get('parent', None)
	if requestBody.get('isApproved', False):
		isApproved = 1
	else:
		isApproved = 0

	if requestBody.get('isHighlighted', False):
		isHighlighted = 1
	else:
		isHighlighted = 0

	if requestBody.get('isEdited', False):
		isEdited = 1
	else:
		isEdited = 0

	if requestBody.get('isSpam', False):
		isSpam = 1
	else:
		isSpam = 0

	if requestBody.get('isDeleted', False):
		isDeleted = 1
	else:
		isDeleted = 0

	sql = """INSERT INTO Post (user, thread, forum, message, parent, date, \
		isSpam, isEdited, isDeleted, isHighlighted, isApproved) VALUES \
		(%(user)s, %(thread)s, %(forum)s, %(message)s, %(parent)s, %(date)s, \
		%(isSpam)s, %(isEdited)s, %(isDeleted)s, %(isHighlighted)s, %(isApproved)s);"""
	args = {'user': user, 'thread': thread, 'forum': forum, 'message': message, 'parent': parent, 'date': date,
			'isSpam': isSpam, 'isEdited': isEdited, 'isDeleted': isDeleted, 'isHighlighted': isHighlighted,
			'isApproved': isApproved}

	postID = db.execute(sql, args, True)
	post = get_post_by_id(postID)
	inc_posts_for_thread(thread)
	if not post:
		return json.dumps({"code": 1, "response": "Empty set"}, indent=4)

	return json.dumps({"code": 0, "response": post}, indent=4)

@module.route("/list/", methods=["GET"])
def list_method():
	qs = get_json(request)

	forum = qs.get('forum')
	thread = qs.get('thread')
	if not forum and not thread:
		return json.dumps({"code": 2, "response": "No 'forum' or 'thread' key"}, indent=4)

	since = qs.get('since', '')
	limit = qs.get('limit', -1)
	order = qs.get('order', '')

	if forum:
		postList = get_post_list(forum=forum, since=since, limit=limit, order=order)
	else:
		postList = get_post_list(thread=thread, since=since, limit=limit, order=order)

	return json.dumps({"code": 0, "response": postList}, indent=4)

@module.route("/details/", methods=["GET"])
def details():
	qs = get_json(request)

	postID = qs.get('post')
	if not postID:
		return json.dumps({"code": 2, "response": "No 'post' key"}, indent=4)

	post = get_post_by_id(postID)
	if not post:
		return json.dumps({"code": 1, "response": "Empty set"}, indent=4)

	relatedValues = list()
	qsRelated = qs.get('related')
	if type(qsRelated) is list:
		relatedValues.extend(qsRelated)
	elif type(qsRelated) is str:
		relatedValues.append(qsRelated)

	threadRelated = False
	forumRelated = False
	userRelated = False
	for relatedValue in relatedValues:
		if relatedValue == 'forum':
			forumRelated = True
		elif relatedValue == 'user':
			userRelated = True
		elif relatedValue == 'thread':
			threadRelated = True
		else:
			return json.dumps({"code": 3, "response": "Wrong related value"}, indent=4)

	if threadRelated:
		post['thread'] = get_thread_by_id(post['thread'])

	if forumRelated:
		post['forum'] = get_forum_dict(short_name=post['forum'])

	if userRelated:
		post['user'] = get_user_dict(post['user'])

	return json.dumps({"code": 0, "response": post}, indent=4)


@module.route("/remove/", methods=["POST"])
def remove():
	requestBody = request.json

	postID = requestBody.get('post')
	post = get_post_by_id(postID)
	threadID = post['thread']

	remove_post(postID)
	dec_posts_for_thread(threadID)

	return json.dumps({"code": 0, "response": {"post": postID}}, indent=4)



@module.route("/restore/", methods=["POST"])
def restore():
	requestBody = request.json

	postID = requestBody.get('post')
	post = get_post_by_id(postID)
	threadID = post['thread']

	restore_post(postID)
	inc_posts_for_thread(threadID)

	return json.dumps({"code": 0, "response": {"post": postID}}, indent=4)


@module.route("/update/", methods=["POST"])
def update():
	requestBody = request.json
	postID = requestBody.get('post')
	message = try_encode(requestBody.get('message'))

	args = {'message': message, 'post': postID}
	db.execute("""UPDATE Post SET message = %(message)s WHERE post = %(post)s;""", args, True)

	post = get_post_by_id(postID)
	if not post:
		return json.dumps({"code": 1, "response": "Empty set"}, indent=4)

	return json.dumps({"code": 0, "response": post}, indent=4)


@module.route("/vote/", methods=["POST"])
def vote():
	requestBody = request.json

	postID = requestBody.get('post')
	voteValue = requestBody.get('vote')

	if voteValue == 1:
		db.execute("""UPDATE Post SET likes = likes + 1, points = points + 1 WHERE post = %(post)s;""",
				   {'post': postID}, True)
	elif voteValue == -1:
		db.execute("""UPDATE Post SET dislikes = dislikes + 1, points = points - 1 WHERE post = %(post)s;""",
				   {'post': postID}, True)
	else:
		return json.dumps({"code": 3, "response": "Wrong 'vote' value'"}, indent=4)

	post = get_post_by_id(postID)
	if not post:
		return json.dumps({"code": 1, "response": "Empty set"}, indent=4)

	return json.dumps({"code": 0, "response": post}, indent=4)