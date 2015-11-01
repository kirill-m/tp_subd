import json, MySQLdb
from MyDB import db
from flask import request, Blueprint
from general_func import try_encode, MYSQL_DUPLICATE_ENTITY_ERROR, get_user_dict, get_json, get_followers_list, \
	get_following_list, get_subscribed_threads_list, get_post_list, str_to_json

module = Blueprint('user', __name__, url_prefix='/db/api/user')

@module.route("/create/", methods=["POST"])
def create():
	requestBody = request.json

	username = try_encode(requestBody.get('username'))
	about = requestBody.get('about')
	name = try_encode(requestBody.get('name'))
	email = requestBody.get('email')
	isAnonymousKey = requestBody.get('isAnonymous', False)
	if isAnonymousKey:
		isAnonymous = 1
	else:
		isAnonymous = 0

	sql = """INSERT INTO User (username, about, name, email, isAnonymous) VALUES \
		(%(username)s, %(about)s, %(name)s, %(email)s, %(isAnonymous)s);"""
	args = {'username': username, 'about': about, 'name': name, 'email': email, 'isAnonymous': isAnonymous}

	try:
		db.execute(sql, args, True)
	except MySQLdb.IntegrityError, message:
		if message[0] == MYSQL_DUPLICATE_ENTITY_ERROR:
			return json.dumps({"code": 5,
							   "response": "This user already exists"}, indent=4)
		return json.dumps({"code": 4,
						   "response": "Oh, we have some really bad error"}, indent=4)

	userDict = get_user_dict(email)

	return json.dumps({"code": 0, "response": userDict}, indent=4)

@module.route("/details/", methods=["GET"])
def details():
	qs = get_json(request)
	email = qs.get('user')
	if not email:
		return json.dumps({"code": 2, "response": "No 'user' key"}, indent=4)

	user = get_user_dict(email)

	user['followers'] = get_followers_list(email)
	user['following'] = get_following_list(email)
	user['subscriptions'] = get_subscribed_threads_list(email)

	return json.dumps({"code": 0, "response": user}, indent=4)

@module.route("/follow/", methods=["POST"])
def follow():
	requestBody = request.json

	follower = requestBody.get('follower')
	followee = requestBody.get('followee')

	args = {'follower': follower, 'following': followee}
	db.execute("""INSERT INTO Follower (follower, following) VALUES (%(follower)s, %(following)s);""", args, True)
	
	return json.dumps({"code": 0, "response": get_user_dict(follower)}, indent=4)


@module.route("/unfollow/", methods=["POST"])
def unfollow():
	requestBody = request.json

	follower = requestBody.get('follower')
	followee = requestBody.get('followee')

	args = {'follower': follower, 'following': followee}
	db.execute("""DELETE FROM Follower WHERE follower = %(follower)s AND following = %(following)s;""", args, True)

	return json.dumps({"code": 0, "response": get_user_dict(follower)}, indent=4)


@module.route("/listPosts/", methods=["GET"])
def listPosts():
	qs = get_json(request)

	email = qs.get('user')
	if not email:
		return json.dumps({"code": 2, "response": "No 'user' key"}, indent=4)

	since = qs.get('since', '')
	limit = qs.get('limit', -1)
	order = qs.get('order', 'desc')

	postList = get_post_list(user=email, since=since, limit=limit, order=order)
	return json.dumps({"code": 0, "response": postList}, indent=4)


@module.route("/listFollowers/", methods=["GET"])
def listFollowers():
	return listFollowers(False)


@module.route("/listFollowing/", methods=["GET"])
def listFollowing():
	return listFollowers(True)


def listFollowers(isFollowing):
	qs = get_json(request)

	email = qs.get('user')
	if not email:
		return json.dumps({"code": 2, "response": "No 'user' key"}, indent=4)

	# Since part
	since_id = qs.get('since_id', -1)
	if since_id != -1:
		sinceSql = """AND User.user >= {}""".format(since_id)
	else:
		sinceSql = ""

	# Order part
	order_sql = """ORDER BY User.name {}""".format(qs.get('order', 'desc'))

	# Limit part
	limit = qs.get('limit', -1)
	if limit != -1:
		try:
			limit = int(limit)
		except ValueError:
			return json.dumps({"code": 3, "response": "Wrong limit value"}, indent=4)
		if limit < 0:
			return json.dumps({"code": 3, "response": "Wrong limit value"}, indent=4)
		limit_sql = """LIMIT {}""".format(limit)
	else:
		limit_sql = ""

	sql = """SELECT about, email, user, isAnonymous, name, username FROM User JOIN Follower ON """
	if not isFollowing:
		sql += """Follower.follower = User.email WHERE Follower.following"""
	else:
		sql += """Follower.following = User.email WHERE Follower.follower"""

	sql += """ = %(email)s {since_value} {order_value} {limit_value};""".format(
		since_value=sinceSql, order_value=order_sql, limit_value=limit_sql)

	userListSql = db.execute(sql, {'email': email})
	if not userListSql:
		return json.dumps({"code": 1, "response": "Empty set"}, indent=4)

	user_list = list()
	for userSql in userListSql:
		followerEmail = str_to_json(userSql[1])
		user_list.append({'about': str_to_json(userSql[0]),
						  'email': followerEmail,
						  'id': str_to_json(userSql[2]),
						  'isAnonymous': str_to_json(userSql[3]),
						  'name': str_to_json(userSql[4]),
						  'username': str_to_json(userSql[5]),
						  'followers': get_followers_list(followerEmail),
						  'following': get_following_list(followerEmail),
						  'subscriptions': get_subscribed_threads_list(followerEmail)})

	return json.dumps({"code": 0, "response": user_list}, indent=4)


@module.route("/updateProfile/", methods=["POST"])
def update_profile():
	requestBody = request.json

	about = try_encode(requestBody.get('about'))
	email = try_encode(requestBody.get('user'))
	name = try_encode(requestBody.get('name'))

	args = {'about': about, 'name': name, 'email': email}
	db.execute("""UPDATE User SET about = %(about)s, name = %(name)s WHERE email = %(email)s;""", args, True)
	return json.dumps({"code": 0, "response": get_user_dict(email)}, indent=4)   