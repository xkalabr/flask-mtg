#!/usr/bin/env python3

import time
import mysql.connector
import urllib.request
import imghdr
import os
import random


cnx = mysql.connector.connect(user='mtgadmin', password='blackL0tus',host='127.0.0.1', database='mtg')
cursor = cnx.cursor()
cursor.execute('SELECT cid,mid FROM cards WHERE mid>0 AND imgpath IS NULL')
rows = cursor.fetchall()
for row in rows:
	print('Fetching ' + str(row[1]) + ' as ' + row[0])
	url = 'http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=' + str(row[1]) + '&type=card'
	websource = urllib.request.urlopen(url)
	data = websource.read()
	file_extension = imghdr.what(None, data)
	print('File type is: ' + str(file_extension))
	if file_extension is None:
		file_extension = jpeg
		print('Unknown file type.  Defaulting to jpeg')
	file_name = row[0]+'.'+file_extension
	pri_dir = file_name[0]
	sec_dir = file_name[1]
	dest_dir = 'images/' + pri_dir + '/' + sec_dir
	if not os.path.isdir(dest_dir):
		os.makedirs(dest_dir)
	full_path = dest_dir + '/' + file_name
	cardImage = open(full_path, 'wb')
	cardImage.write(data)
	cardImage.close()
	cursor2 = cnx.cursor()
	cursor2.execute('UPDATE cards SET imgpath="' + full_path + '" where cid="' + row[0] + '"')
	cursor2.close()
	cnx.commit()
	time.sleep(random.randint(1,10))
cursor.close()
cnx.close()

