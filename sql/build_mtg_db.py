#!/usr/bin/env python3

import json
import mysql.connector

cnx = mysql.connector.connect(user='mtgadmin', password='blackL0tus',host='127.0.0.1', database='mtg')


counter_order = ['sets','cards','altnames','colors','colorids','types','supertypes','subtypes','variations','rulings']
counters = {'sets': {'dispName': 'Sets', 'counter': 0, 'table': 'cardsets'}, 'cards':  {'dispName': 'Cards', 'counter': 0, 'table': 'cards'}, 'altnames': {'dispName': 'AltNames', 'counter': 0, 'table': 'altnames'}, 'colors': {'dispName': 'Colors', 'counter': 0, 'table': 'colors'}, 'colorids': {'dispName': 'ColorIds', 'counter': 0, 'table': 'colorids'}, 'types': {'dispName': 'Types', 'counter': 0, 'table': 'cardtypes'}, 'supertypes': {'dispName': 'SuperTypes', 'counter': 0, 'table': 'cardsupertypes'}, 'subtypes': {'dispName': 'SubTypes', 'counter': 0, 'table': 'cardsubtypes'}, 'variations': {'dispName': 'Variations', 'counter': 0, 'table': 'cardvariations'}, 'rulings': {'dispName': 'Rulings', 'counter': 0, 'table': 'rulings'} } 

with open('AllPrintings.json') as data_file:
	data = json.load(data_file)

# Sort the sets by releaseDate
dates = []
sets = data.keys()
for scode in sets:
	rdate = data[scode].get('releaseDate')
	dates.append(rdate)
sorted_sets = sorted(list(zip(sets,dates)), key=lambda x: x[1])
unzipped = list(zip(*sorted_sets))
sets = list(unzipped[0])


for scode in sets:
	if data[scode].get('type') in ['core', 'duel_deck', 'expansion', 'masters']:
		if data[scode].get('isOnlineOnly'):
			continue
		counters['sets']['counter'] += 1
		cursor = cnx.cursor()
		s_name = data[scode].get('name', '***BAD DATA***').replace('"', '\\"')
		s_reldate = data[scode].get('releaseDate', '***BAD DATA***')
		s_type = data[scode].get('type', '')
		s_block = data[scode].get('block', '')
		sql = 'INSERT INTO cardsets (id, code, name, reldate, type, block) VALUES (null,"' + scode + '","' + s_name + '","' + s_reldate + '","' + s_type + '","' + s_block +'")'
		cursor.execute(sql)
		cursor.close()
		cnx.commit()
		cards = sorted(data[scode]['cards'], key=lambda x: x['uuid'])
		for c in cards:
			counters['cards']['counter'] += 1
			c_id = c.get('uuid', '***BAD DATA***')
			c_layout = c.get('layout')
			c_name = c.get('name', '***BAD DATA***').replace('"', '\\"')
			ca_altnames = c.get('names', '')
			c_manaCost = c.get('manaCost', '')
			c_cmc = str(c.get('convertedManaCost', ''))
			ca_colors = c.get('colors', '')
			ca_colorId = c.get('colorIdentity', '')
			c_type = c.get('type', '')
			ca_types = c.get('types', '')
			ca_supertypes = c.get('supertypes', '')
			ca_subtypes = c.get('subtypes', '')
			c_rarity = c.get('rarity')
			c_text = c.get('text', '').replace('"', '\\"')
			c_flavor = c.get('flavor', '').replace('"', '\\"')
			c_artist = c.get('artist', '')
			c_number = str(c.get('number', ''))
			c_power = str(c.get('power', ''))
			c_tough = str(c.get('toughness', ''))
			c_loyal = str(c.get('loyalty', ''))
			c_multiId = str(c.get('multiverseid', '0'))
			ca_variations = c.get('variations', '')
			ca_rulings = c.get('rulings', '')

			try:
				cursor = cnx.cursor()
				sql = 'INSERT INTO cards (cid, layout, name, manacost, cmc, type, rarity, ctext, ftext, artist, num, p, t, l, mid, imgpath, setcode) VALUES ("' + c_id + '","' + c_layout + '","' + c_name + '","' + c_manaCost + '","' + c_cmc + '","' + c_type + '","' + c_rarity + '","' + c_text + '","' + c_flavor + '","' + c_artist + '","' + c_number + '","' + c_power + '","' + c_tough + '","' + c_loyal + '","' + c_multiId + '",null,"' + scode + '")'
				cardsql = sql
				#print('CARD: ' + sql)
				cursor.execute(sql)
				for val in ca_altnames:
					counters['altnames']['counter'] += 1
					sql = 'INSERT INTO altnames (id, cid, name) VALUES (null,"' + c_id + '","' + val + '")'
					#print('ALTNAMES: ' + sql)
					cursor.execute(sql)

				for val in ca_colors:
					counters['colors']['counter'] += 1
					sql = 'INSERT INTO colors (id, cid, color) VALUES (null,"' + c_id + '","' + val + '")'
					#print('COLORS: ' + sql)
					cursor.execute(sql)

				for val in ca_colorId:
					counters['colorids']['counter'] += 1
					sql = 'INSERT INTO colorids (id, cid, colorid) VALUES (null,"' + c_id + '","' + val + '")'
					#print('COLORIDS: ' + sql)
					cursor.execute(sql)

				for val in ca_types:
					counters['types']['counter'] += 1
					sql = 'INSERT INTO cardtypes (id, cid, ctype) VALUES (null,"' + c_id + '","' + val + '")'
					#print('TYPES: ' + sql)
					cursor.execute(sql)

				for val in ca_supertypes:
					counters['supertypes']['counter'] += 1
					sql = 'INSERT INTO cardsupertypes (id, cid, csuptype) VALUES (null,"' + c_id + '","' + val + '")'
					#print('SUPERTYPES: ' + sql)
					cursor.execute(sql)

				for val in ca_subtypes:
					counters['subtypes']['counter'] += 1
					sql = 'INSERT INTO cardsubtypes (id, cid, csubtype) VALUES (null,"' + c_id + '","' + val + '")'
					#print('SUBTYPES: ' + sql)
					cursor.execute(sql)

				for val in ca_variations:
					counters['variations']['counter'] += 1
					sql = 'INSERT INTO cardvariations (id, cid, cvars) VALUES (null,"' + c_id + '","' + str(val) + '")'
					#print('VARIATIONS: ' + sql)
					cursor.execute(sql)

				for val in ca_rulings:
					counters['rulings']['counter'] += 1
					myDate = val.get('date')
					myText = val.get('text').replace('"', '\\"')
					sql = 'INSERT INTO rulings (id, cid, rdate, rtext) VALUES (null,"' + c_id + '","' + myDate + '","' + myText + '")'
					#print('RULINGS: ' + sql)
					cursor.execute(sql)

				cursor.close()
				cnx.commit()
			except mysql.connector.errors.Error as e:
				print('Transaction failed, rolling back.  Error was:')
				print(e.args)
				print(cardsql)
				try:
					cnx.rollback()
				except:
					pass
cursor = cnx.cursor()
print('Verification Stage:')
for cnt in counter_order:
	cursor.execute('SELECT COUNT(*) FROM ' + counters[cnt]['table'])
	val = cursor.fetchone()
	if val[0] == counters[cnt]['counter']:
		print(counters[cnt]['dispName'] + ': Passed (' + str(val[0]) + ')')
	else:
		print(counters[cnt]['dispName'] + ': Failed --- Expected: ' + str(counters[cnt]['counter']) + '  Found: ' + str(val[0]))


cursor.close()
cnx.close()
