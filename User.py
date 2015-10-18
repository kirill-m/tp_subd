import json, MySQLdb
from MyDB import db
from flask import request, Blueprint

module = Blueprint('user', __name__, url_prefix='/db/api/user')

@module.route("/create/", methods=["POST"])
def create():
    request_body = request.json
    return "todo"

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