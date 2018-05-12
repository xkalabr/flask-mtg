from flask import Flask, jsonify, request
from sqlalchemy import create_engine
app = Flask(__name__)
engine = create_engine('mysql+mysqlconnector://mtgadmin:blackL0tus@localhost/mtg')

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
	result = engine.execute('select code,name from cardsets order by reldate desc')
	for row in result:
		retval.append({'code': row[0], 'name': row[1]})
	return jsonify(retval)

@app.route("/card/<string:cid>")
def show_card(cid):
	retval = {'cid': cid}
	sql = (
		'select c.name, manacost, c.type, rarity, ctext, ftext, p, t, l, imgpath, setcode, '
		'cardsets.name from cards as c,cardsets where cid=\'' + cid + '\' and code=setcode'
	)
	result = engine.execute(sql)
	for row in result:
		retval['name'] = row[0]
		retval['manacost'] = row[1]
		retval['type'] = row[2]
		retval['rarity'] = row[3]
		retval['ctext'] = row[4]
		retval['ftext'] = row[5]
		retval['p'] = row[6]
		retval['t'] = row[7]
		retval['l'] = row[8]
		if row[9] is not None:
			ipath = row[9].split('/')
			retval['imgpath'] = ipath[3]
		else:
			retval['imgpath'] =  ''
		retval['setcode'] = row[10]
		retval['setname'] = row[11]
	return jsonify(retval)

@app.route("/cardsearch/<string:term>")
def card_search(term):
	retval = []
	sql = (
		'select cid,c.name,rarity,setcode,s.name from cards as c, cardsets as s where '
		'code=setcode and c.name like "%' + term + '%"'
	)
	result = engine.execute(sql)
	for row in result:
		entry = {}
		entry['cid'] = row[0]
		entry['name'] = row[1]
		entry['rarity'] = row[2]
		entry['setcode'] = row[3]
		entry['setname'] = row[4]
		retval.append(entry)
	return jsonify(retval)