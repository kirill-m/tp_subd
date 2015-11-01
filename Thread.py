import json, MySQLdb
from MyDB import db
from flask import request, Blueprint
from general_func import get_json, get_thread_list, try_encode, get_forum_dict, get_user_dict, get_post_list, remove_post, \
	restore_post, str_to_json, get_thread_by_id, MYSQL_DUPLICATE_ENTITY_ERROR

module = Blueprint('thread', __name__, url_prefix='/db/api/thread')


@module.route("/close/", methods=["POST"])
def close():
	thread = request.json.get('thread')
	db.execute("""UPDATE Thread SET isClosed = 1 WHERE thread = %(thread)s;""", {'thread': thread}, True)
	return json.dumps({"code": 0, "response": thread}, indent=4)


@module.route("/create/", methods=["POST"])
def create():
	requestBody = request.json
	
	# Required
	forum = requestBody.get('forum')
	title = try_encode(requestBody.get('title'))
	if requestBody.get('isClosed'):
		is_closed = 1
	else:
		is_closed = 0
	user = requestBody.get('user')
	date = requestBody.get('date')
	message = requestBody.get('message')
	slug = requestBody.get('slug')

	# Optional
	if requestBody.get('isDeleted', False):
		isDeleted = 1
	else:
		isDeleted = 0

	sql = """INSERT INTO Thread (forum, title, isClosed, user, date, message, slug, isDeleted) \
		VALUES (%(forum)s, %(title)s, %(isClosed)s, %(user)s, %(date)s, %(message)s, %(slug)s, %(isDeleted)s);"""
	args = {'forum': forum, 'title': title, 'isClosed': is_closed, 'user': user, 'date': date, 'message': message,
			'slug': slug, 'isDeleted': isDeleted}

	try:
		db.execute(sql, args, True)
	except MySQLdb.IntegrityError, message:
		print message[0]
	finally:
		threadList = get_thread_list(title=title)
		if threadList == list():
			return json.dumps({"code": 1, "response": "Empty set"}, indent=4)

		return json.dumps({"code": 0, "response": threadList[0]}, indent=4)


@module.route("/details/", methods=["GET"])
def details():
	qs = get_json(request)

	threadID = qs.get('thread')
	if not threadID:
		return json.dumps({"code": 2, "response": "No 'thread' key"}, indent=4)

	thread = get_thread_by_id(threadID)
	if thread == list():
		return json.dumps({"code": 1, "response": "Empty set"}, indent=4)

	relatedValues = list()
	qsRelated = qs.get('related')
	if type(qsRelated) is list:
		relatedValues.extend(qsRelated)
	elif type(qsRelated) is str:
		relatedValues.append(qsRelated)

	forumRelated = False
	userRelated = False
	for relatedValue in relatedValues:
		if relatedValue == 'forum':
			forumRelated = True
		elif relatedValue == 'user':
			userRelated = True
		else:
			return json.dumps({"code": 3, "response": "Wrong related value"}, indent=4)

	if forumRelated:
		thread['forum'] = get_forum_dict(short_name=thread['forum'])

	if userRelated:
		thread['user'] = get_user_dict(thread['user'])

	return json.dumps({"code": 0, "response": thread}, indent=4)


@module.route("/list/", methods=["GET"])
def list_method():
	qs = get_json(request)
	if qs.get('forum'):
		key = "forum"
	elif qs.get('user'):
		key = "user"
	else:
		return json.dumps({"code": 2, "response": "No 'forum' key"}, indent=4)
	keyValue = qs.get(key)

	since = qs.get('since', '')
	order = qs.get('order', '')
	limit = qs.get('limit', -1)

	if key == "forum":
		threadList = get_thread_list(forum=keyValue, since=since, order=order, limit=limit)
	else:
		threadList = get_thread_list(user=keyValue, since=since, order=order, limit=limit)

	return json.dumps({"code": 0, "response": threadList}, indent=4)


@module.route("/listPosts/", methods=["GET"])
def list_posts():
	qs = get_json(request)

	thread = qs.get('thread')
	since = qs.get('since', '')
	limit = qs.get('limit', -1)
	order = qs.get('order', 'desc')
	sort = qs.get('sort', 'flat')

	postList = get_post_list(thread=thread, since=since, limit=limit, sort=sort, order=order)

	return json.dumps({"code": 0, "response": postList}, indent=4)


@module.route("/open/", methods=["POST"])
def open_route():
	thread = request.json.get('thread')
	db.execute("""UPDATE Thread SET isClosed = 0 WHERE thread = %(thread)s;""", {'thread': thread}, True)
	return json.dumps({"code": 0, "response": thread}, indent=4)


@module.route("/remove/", methods=["POST"])
def remove():
	requestBody = request.json

	thread = requestBody.get('thread')
	postList = get_post_list(thread=thread)
	for post in postList:
		remove_post(post['id'])

	db.execute("""UPDATE Thread SET isDeleted = 1, posts = 0 WHERE thread = %(thread)s;""", {'thread': thread}, True)

	return json.dumps({"code": 0, "response": thread}, indent=4)


@module.route("/restore/", methods=["POST"])
def restore():
	thread = request.json.get('thread')

	postList = get_post_list(thread=thread)
	for post in postList:
		restore_post(post['id'])

	db.execute("""UPDATE Thread SET isDeleted = 0, posts = %(posts)s WHERE thread = %(thread)s;""",
			   {'posts': len(postList), 'thread': thread}, True)

	return json.dumps({"code": 0, "response": thread}, indent=4)


@module.route("/subscribe/", methods=["POST"])
def subscribe():
	requestBody = request.json

	user = requestBody.get('user')
	thread = requestBody.get('thread')
	try:
		db.execute("""INSERT INTO Subscription (subscriber, thread) VALUES (%(subscriber)s, %(thread)s);""",
				   {'subscriber': user, 'thread': thread}, True)
	except MySQLdb.IntegrityError, message:
		if message[0] == MYSQL_DUPLICATE_ENTITY_ERROR:
			print "Already subscribed"
	
	resultDict = {'thread': thread, 'user': str_to_json(user)}
	return json.dumps({"code": 0, "response": resultDict}, indent=4)


@module.route("/unsubscribe/", methods=["POST"])
def unsubscribe():
	requestBody = request.json

	user = requestBody.get('user')
	thread = requestBody.get('thread')
	db.execute("""DELETE FROM Subscription WHERE subscriber = %(subscriber)s AND thread = %(thread)s;""",
		   {'subscriber': user, 'thread': thread}, True)

	resultDict = {'thread': thread, 'user': str_to_json(user)}
	return json.dumps({"code": 0, "response": resultDict}, indent=4)


@module.route("/update/", methods=["POST"])
def update():
	requestBody = request.json

	message = requestBody.get('message')
	slug = requestBody.get('slug')
	threadID = requestBody.get('thread')

	db.execute("""UPDATE Thread SET message = %(message)s, slug = %(slug)s WHERE thread = %(thread)s;""",
			   {'message': message, 'slug': slug, 'thread': threadID}, True)
	return json.dumps({"code": 0, "response": get_thread_by_id(threadID)}, indent=4)


@module.route("/vote/", methods=["POST"])
def vote():
	requestBody = request.json

	voteValue = requestBody.get('vote')
	threadID = requestBody.get('thread')

	if voteValue == 1:
		db.execute("""UPDATE Thread SET likes = likes + 1, points = points + 1 WHERE thread = %(thread)s;""",
				   {'thread': threadID}, True)
	else:
		db.execute("""UPDATE Thread SET dislikes = dislikes + 1, points = points - 1 WHERE thread = %(thread)s;""",
				   {'thread': threadID}, True)
	return json.dumps({"code": 0, "response": get_thread_by_id(threadID)}, indent=4)