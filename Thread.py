import json, MySQLdb
from MyDB import db
from flask import request, Blueprint

module = Blueprint('thread', __name__, url_prefix='/db/api/thread')

@module.route("/create/", methods=["POST"])
def create():
    request_body = request.json
    return "todo"

@module.route("/list/", methods=["GET"])
def list():
    return "todo"

@module.route("/details/", methods=["GET"])
def details():
    return "todo"

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