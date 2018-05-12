from flask import Flask, jsonify, request
import mysql.connector
app = Flask(__name__)
cnx = mysql.connector.connect(user='mtgadmin', password='blackL0tus',host='127.0.0.1', database='mtg')

IMAGE_BASE_PATH = '../mtg/images/'

@app.route("/cardimage/<string:filename>")
def show_image(filename):
	firstChar = filename[0]
	secondChar = filename[1]
	f = open(IMAGE_BASE_PATH + firstChar + '/' + secondChar + '/' + filename, 'rb')
	myPic = f.read()
	f.close()
	return myPic

@app.route("/cardsets")
def list_sets():
	retval = []
	cursor = cnx.cursor()
	cursor.execute('select code,name from cardsets order by reldate desc')
	result = cursor.fetchall()
	for row in result:
		retval.append({'code': row[0], 'name': row[1]})
	return jsonify(retval)

