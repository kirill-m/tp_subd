import json, MySQLdb
from flask import request, Blueprint
from general_func import get_forum_dict, get_json, get_user_dict, get_subscribed_threads_list, \
	get_post_list, get_thread_list, str_to_json, get_thread_by_id, db

module = Blueprint('forum', __name__, url_prefix='/db/api/forum')


@module.route("/create/", methods=["POST"])
def create():
	requestBody = request.json

	name = requestBody.get('name')
	short_name = requestBody.get('short_name')
	user = requestBody.get('user')

	try:
		db.execute("""INSERT INTO Forum (name, short_name, user) VALUES (%(name)s, %(short_name)s, %(user)s);""",
				   {'name': name, 'short_name': short_name, 'user': user}, True)
	except MySQLdb.IntegrityError, message:
		print message[0]
	finally:
		forumDict = get_forum_dict(short_name=short_name)
		return json.dumps({"code": 0, "response": forumDict}, indent=4)


@module.route("/details/", methods=["GET"])
def details():
    qs = get_json(request)
    short_name = qs.get('forum')

    if not short_name:
        return json.dumps({"code": 2, "response": "No 'forum' key"}, indent=4)

    forumDict = get_forum_dict(short_name=short_name)
    if not forumDict:
        return json.dumps({"code": 1, "response": "Empty set"}, indent=4)

    if qs.get('related', '') == 'user':
        forumDict['user'] = get_user_dict(forumDict['user'])

    return json.dumps({"code": 0, "response": forumDict}, indent=4)


@module.route("/listPosts/", methods=["GET"])
def listPosts():
	qs = get_json(request)
	forum = qs.get('forum')

	if not forum:
		return json.dumps({"code": 2, "response": "No 'forum' key"}, indent=4)

	# Related part
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
		if relatedValue == 'thread':
			threadRelated = True
		elif relatedValue == 'forum':
			forumRelated = True
		elif relatedValue == 'user':
			userRelated = True
		else:
			return json.dumps({"code": 3, "response": "Wrong related value"}, indent=4)

	since = qs.get('since', '')
	limit = qs.get('limit', -1)
	sort = qs.get('sort', 'flat')
	order = qs.get('order', 'desc')

	postList = get_post_list(forum=forum, since=since, limit=limit, sort=sort, order=order)

	for post in postList:
		if userRelated:
			post['user'] = get_user_dict(post['user'])

		if threadRelated:
			post['thread'] = get_thread_by_id(post['thread'])

		if forumRelated:
			post['forum'] = get_forum_dict(short_name=post['forum'])

	return json.dumps({"code": 0, "response": postList}, indent=4)


@module.route("/listThreads/", methods=["GET"])
def listThreads():
	qs = get_json(request)

	forum = qs.get('forum')

	if not forum:
		return json.dumps({"code": 2, "response": "No 'forum' key"}, indent=4)

	since = qs.get('since', '')
	order = qs.get('order', '')
	limit = qs.get('limit', -1)
	threadList = get_thread_list(forum=forum, since=since, order=order, limit=limit)

	# Related part
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

	for thread in threadList:
		if userRelated:
			thread['user'] = get_user_dict(thread['user'])
			thread['user']['subscriptions'] = get_subscribed_threads_list(thread['user']['email'])

		if forumRelated:
			thread['forum'] = get_forum_dict(short_name=thread['forum'])

	return json.dumps({"code": 0, "response": threadList}, indent=4)
	

@module.route("/listUsers/", methods=["GET"])
def listUsers():
	qs = get_json(request)

	if not qs.get('forum'):
		return json.dumps({"code": 2, "response": "No 'forum' key"}, indent=4)

	# Since id part
	since_id = qs.get('since_id')
	if since_id:
		try:
			since_id = int(since_id)
		except ValueError:
			return json.dumps({"code": 3, "response": "Wrong since_id value"}, indent=4)
		since_id_sql = """AND User.user >= {}""".format(since_id)
	else:
		since_id_sql = ''

	# Limit part
	if qs.get('limit'):
		limit = qs.get('limit')[0]
		try:
			limit = int(limit)
		except ValueError:
			return json.dumps({"code": 3, "response": "Wrong limit value"}, indent=4)
		if limit < 0:
			return json.dumps({"code": 3, "response": "Wrong limit value"}, indent=4)
		limit_sql = """LIMIT {}""".format(limit)
	else:
		limit_sql = ''

	# Order part
	order = qs.get('order', 'desc')
	order_sql = """ORDER BY User.name {}""".format(order)

	sql = """SELECT User.user, User.email, User.name, User.username, User.isAnonymous, User.about FROM User \
		WHERE User.email IN (SELECT DISTINCT user FROM Post WHERE forum = %(forum)s) {snc_sql} {ord_sql} \
		{lim_sql};""".format(snc_sql=since_id_sql, lim_sql=limit_sql, ord_sql=order_sql)

	userListSql = db.execute(sql, {'forum': qs.get('forum')})

	userList = list()
	for userSql in userListSql:
		email = str_to_json(userSql[1])
		userList.append({'id': str_to_json(userSql[0]),
						  'email': email,
						  'name': str_to_json(userSql[2]),
						  'username': str_to_json(userSql[3]),
						  'isAnonymous': str_to_json(userSql[4]),
						  'about': str_to_json(userSql[5]),
						  'subscriptions': get_subscribed_threads_list(email)})

	return json.dumps({"code": 0, "response": userList}, indent=4)
