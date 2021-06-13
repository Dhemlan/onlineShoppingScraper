import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv

import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

def get_db_cursor():
    database = r"onlineShopping.db"
    conn = create_connection(database)

    try:	
        cursor = conn.cursor()
    except Error as e:
        print(e)

    return cursor
    



header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}

with open('wishlist') as f:

	brokenItems = []
	tenOff = []
	twentyOff = []
	thirtyOff = []
	fortyOff = []
	fiftyPlusOff = []

	summaryDict = {
		"50+ off" : fiftyPlusOff,
		"40 off" : fortyOff,
		"30 off" : thirtyOff,
		"20 off" : twentyOff,
		"10 off" : tenOff,
		"Broken items" : brokenItems
	}

	# Row constants
	ITEM = 0
	BASE_PRICE = 1
	STORE = 2
	TAG = 3
	ARGS = 4
	VALUE = 5
	URL = 6

	cursor = get_db_cursor()
	cursor.execute("SELECT item.name, basePrice, store, tag, args, value, url FROM stock JOIN item on item.name=item JOIN store on store=store.name")
	rows = cursor.fetchall()
	for row in rows:
		k = requests.get(row[URL], headers = header).text
		soup = BeautifulSoup(k,'html.parser')
		tag = '%s' % row[TAG]
		myDict = {row[ARGS]:row[VALUE]}
		result = soup.findAll(tag, attrs=myDict)
		prefix = row[ITEM] + " from " + row[STORE]
		if not result :
			brokenItems.append(prefix)
		else:
			for node in result:
				priceFound = ''.join(node.findAll(text=True)).strip('$')
				discount = round((row[BASE_PRICE] - float(priceFound)) / row[BASE_PRICE] * 100, 2)
				output = prefix + ": $" + str(priceFound) + " - " + str(discount) + "% off (usual price: $" + str(row[BASE_PRICE]) + ")"
				#print("test" + output)
				if (discount > 50):
					fiftyPlusOff.append(output)
				elif (discount > 40):
					fortyOff.append(output)
				elif (discount > 30):
					thirtyOff.append(output)
				elif (discount > 20):
					twentyOff.append(output)
				elif (discount > 10):
					tenOff.append(output)



	for key in summaryDict :
		print()
		print(key)
		print("==========")
		for item in summaryDict[key]:
			print(item)
		print()
