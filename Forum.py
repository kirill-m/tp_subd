import json, MySQLdb
from MyDB import db
from flask import request, Blueprint

module = Blueprint('forum', __name__, url_prefix='/db/api/forum')


@module.route("/create/")
def create():
    request_body = request.json
    return "todo"

@module.route("/details/", methods=["GET"])
def details():
    return "todo"

@module.route("/listPosts/", methods=["GET"])
def listPosts():
    return  "todo"

@module.route("/listThread/", methods=["GET"])
def listThread():
    return "todo"

@module.route("/listUsers/", methods=["GET"])
def listUsers():
    return "todo"

           