import json, urllib, urlparse
from flask import Flask, request
from flaskext.mysql import MySQL
import index, MySQLdb

# from Entities.MyDatabase import db
# from Entities.Forum import module as forum_module
# from Entities.Post import module as post_module
# from Entities.User import module as user_module
# from Entities.Thread import module as thread_module


app = Flask(__name__)
mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'root'
#app.config['MYSQL_DATABASE_PASSWORD'] = 'secret'
app.config['MYSQL_DATABASE_DB'] = 'rk1'
#app.config['MYSQL_DATABASE_PORT'] = 9000
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

conn = mysql.connect()
cursor = conn.cursor()

@app.route('/')
def index_def():
	url = dict((k, v if len(v) > 1 else v[0]) for k, v in urlparse.parse_qs(request.query_string).iteritems())
	print(url)
	name = request.args.get('name')
	quer = "SELECT * from Highschooler"
	cursor.execute(quer)
	data = cursor.fetchone()
	while data is not None:
  		print(data)
  		data = cursor.fetchone()
	return request.query_string 

@app.route('/insert')
def insert():
	name = request.args.get('name')
	query = "INSERT INTO Likes VALUES ('1','3')"
	print('1: ' + query)
	cursor.execute(query)
	data = cursor.fetchone()
	print(data)
	conn.commit()
	return "tbl " + 'created'

@app.route('/create')
def create():
	#name = request.args.get('name')
	name = 'New'
	query = """CREATE TABLE Lol (fn CHAR(20))"""
	
	#print('1: ' + query + "name =  " + name)
	cursor.execute(query, (name,))
	#data = cursor.fetchone()
	#print(data)
	#conn.commit()
	#cursor.close()
	#conn.close()
	return 'lol ' + query	

# if __name__ == '__main__':
# 	app.run(debug=True)