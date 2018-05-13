#!/usr/bin/env python3

import os
import mysql.connector

cnx = mysql.connector.connect(user='mtgadmin', password='blackL0tus',host='127.0.0.1', database='mtg')
for root, dirs, files in os.walk('images'):
	for f in files:
		card_id = f.split('.')
		full_path = root + '/' + f
		cursor = cnx.cursor()
		cursor.execute('UPDATE cards SET imgpath="' + full_path + '" where cid="' + card_id[0] + '"')
		cursor.close()
		cnx.commit()
cnx.close()

