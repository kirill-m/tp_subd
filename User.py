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

@app.route("/follow/", methods=["POST"])
def follow():
    return "todo"

@app.route("/unfollow/", methods=["POST"])
def unfollow():
    return  "todo"

@app.route("/listPosts/", methods=["GET"])
def listPosts():
    return "todo"

@app.route("/updateProfile/", methods=["POST"])
def updateProfile():
    return "todo"

@app.route("/listFollowers/", methods=["GET"])
def listFollowers():
    return "todo"

@app.route("/listFollowing/", methods=["GET"])
def listFollowing():
    return "todo"   