import json
import MySQLdb
from flask import request


@app.route("/create/", methods=["POST"])
def create():
    request_body = request.json
    return "todo"

@app.route("/list/", methods=["GET"])
def list():
    return "todo"

@app.route("/details/", methods=["GET"])
def details():
    return "todo"

@app.route("/remove/", methods=["POST"])
def remove():
    return "todo"

@app.route("/open/", methods=["POST"])
def open():
    return  "todo"

@app.route("/close/", methods=["POST"])
def close():
    return "todo"

@app.route("/listPosts/", methods=["GET"])
def listPosts():
    return "todo"

@app.route("/update/", methods=["POST"])
def update():
    return "todo"

@app.route("/subscribe/", methods=["POST"])
def subscribe():
    return "todo"

@app.route("/unsubscribe/", methods=["POST"])
def unsubscribe():
    return "todo"

@app.route("/vote/", methods=["POST"])
def vote():
    return "todo"