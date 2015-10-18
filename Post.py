import json, MySQLdb
from MyDB import db
from flask import request, Blueprint

module = Blueprint('post', __name__, url_prefix='/db/api/post')

@module.route("/create/", methods=["POST"])
def create():
    request_body = request.json
    return "todo"

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