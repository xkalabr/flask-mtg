from flask import Flask, jsonify, request
from sqlalchemy import create_engine
from mtgdb.model.inventory import Inventory, InventorySchema
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

@app.route('/card/<string:id>', methods=['DELETE'])
def delete_card(id):
	sql = 'delete from inventory where id=' + id
	engine.execute(sql)
	return '', 204

@app.route('/card/', methods=['POST'])
def add_card():
	card = InventorySchema().load(request.get_json())
	indeck = 0
	isfoil = 0
	if card.data.indeck:
		indeck = 1
	if card.data.isfoil:
		isfoil = 1
	sql = (
		'insert into inventory (cid,price,cond,indeck,isfoil) values (\'' + card.data.cid + '\''
		',' + str(card.data.price) + ',' + str(card.data.cond) + ',' + str(indeck) + ','
		+ str(isfoil) + ')'
	)
	engine.execute(sql)
	return "", 204

@app.route('/card/<string:id>', methods=['PUT'])
def update_card(id):
	card = InventorySchema().load(request.get_json())
	indeck = 0
	isfoil = 0
	if card.data.indeck:
		indeck = 1
	if card.data.isfoil:
		isfoil = 1
	sql = (
		'update inventory set price=' + str(card.data.price) + ',cond=' + str(card.data.cond)
		 + ',indeck=' + str(indeck) + ',isfoil=' + str(isfoil) + ' where id=' + id
	)
	engine.execute(sql)
	return "", 204	

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

@app.route("/cardinventory/<string:cid>")
def card_inventory(cid):
	retval = {'stock': [], 'foil': [], 'deck': []}
	sql = (
		'select i.id,name,price,condval,indeck,isfoil from inventory as i,cardcondition '
		'as cc,cards as c where i.cid=\'' + cid + '\' and cond=cc.id and i.cid=c.cid '
		'order by cc.id'
	)
	result = engine.execute(sql)
	for row in result:
		entry = {}
		entry['id'] = row[0]
		entry['name'] = row[1]
		entry['price'] = str(row[2])
		entry['cond'] = row[3]
		indeck = row[4]
		isfoil = row[5]
		if indeck:
			retval['deck'].append(entry)
		elif isfoil:
			retval['foil'].append(entry)
		else:
			retval['stock'].append(entry)
	return jsonify(retval)

@app.route("/setinventory/<string:id>")
def set_inventory(id):
	retval = []
	sql = (
		'select count(i.id),ANY_VALUE(c.cid),c.name,ANY_VALUE(c.type),ANY_VALUE(rarity),'
		'ANY_VALUE(price),ANY_VALUE(code) from cards as c join cardsets on setcode=code left '
		'join inventory as i on i.cid=c.cid where code=\'' + id + '\' group by c.name order '
		'by c.name'
	)
	result = engine.execute(sql)
	for row in result:
		entry = {}
		entry['num'] = row[0]
		entry['cid'] = row[1]
		entry['name'] = row[2]
		entry['type'] = row[3]
		entry['rarity'] = row[4]
		if row[5] is None:
			entry['price'] = '0.00'
		else:
			entry['price'] = str(row[5])
		entry['setcode'] = row[6]
		res = engine.execute('select color from colors where cid=\'' + row[1] + '\'')
		e = []
		for r in res:
			e.append(r[0])
		if len(e) < 1:
			e.append('None')
		entry['color'] = e
		retval.append(entry)
	return jsonify(retval)