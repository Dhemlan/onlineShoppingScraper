import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv

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
	ITEM_CATEGORY = 1
	RRP = 2
	STORE = 3
	TAG = 4
	ATTRIBUTE = 5
	VALUE = 6
	URL = 7



	reader = csv.reader(f, delimiter=',', escapechar='\\')
	for row in reader:
		k = requests.get(row[URL], headers = header).text
		soup = BeautifulSoup(k,'html.parser')
		tag = '%s' % row[TAG]
		myDict = {row[ATTRIBUTE]:row[VALUE]}
		result = soup.findAll(tag, attrs=myDict)
		prefix = row[ITEM] + " from " + row[STORE]
		if not result :
			brokenItems.append(prefix)
		else:
			for node in result:
				priceFound = ''.join(node.findAll(text=True)).strip('$')
				discount = round((float(row[RRP]) - float(priceFound)) / float(row[RRP]) * 100, 2)
				output =prefix + ": $" + str(priceFound) + " - " + str(discount) + "% off (usual price: $" + row[RRP] + ")"
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
