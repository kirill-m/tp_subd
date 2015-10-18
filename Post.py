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

@app.route("/remove/", methods=["POST"])
def remove():
    return "todo"

@app.route("/restore/", methods=["POST"])
def restore():
    return "todo"

@app.route("/update/", methods=["POST"])
def update():
    return  "todo"

@app.route("/vote/", methods=["GET"])
def vote():
    return "todo" 