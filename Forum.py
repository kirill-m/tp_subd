import json
import MySQLdb
from flask import request


@app.route("/create/", methods=["POST"])
def create():
    request_body = request.json
    return "todo"

@app.route("/details/", methods=["GET"])
def details():
    return "todo"

@app.route("/listPosts/", methods=["GET"])
def listPosts():
    return  "todo"

@app.route("/listThread/", methods=["GET"])
def listThread():
    return "todo"

@app.route("/listUsers/", methods=["GET"])
def listUsers():
    return "todo"

           