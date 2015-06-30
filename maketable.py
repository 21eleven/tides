import sys
import timeit
start = timeit.default_timer()
import time
import requests
import json
import pandas as pd
from subprocess import Popen, PIPE
import pymongo
import numpy as np
from bson import json_util
from pymongo import MongoClient
import optparse

parser = optparse.OptionParser('set one of the following flags: -s <seconds ago> or -m <minutes ago>')

parser.add_option('-s', dest='seconds_ago', type='string', help='specify how long ago in SECONDS')
parser.add_option('-m', dest='min_ago', type='string', help='specify how long ago in MINUTES')
(options, args) = parser.parse_args()

client = MongoClient('localhost', 27017)
db = client['tides']

if options.min_ago:
	options.seconds_ago= int(options.min_ago) * 6

seconds_ago = options.seconds_ago

if options.seconds_ago:
	collection = db.books
	current = Popen(['date','+%s'], stdout=PIPE).communicate()
	current_int = int((''.join(map(str,current))[:10]))
	time = current_int - int(seconds_ago)
	print time
	bids = [json.dumps(bid, default=json_util.default) for bid in collection.find({"reqtimestamp" : {"$lt":time, "$gte":time-300}, "type":"bid"}).sort("price",pymongo.DESCENDING)];
	asks = [json.dumps(ask, default=json_util.default) for ask in collection.find({"reqtimestamp" : {"$lt":time, "$gte":time-300}, "type":"ask"}).sort("price",pymongo.ASCENDING)];

else:
	collection = db.currentbook


	bids = [json.dumps(bid, default=json_util.default) for bid in collection.find({"type":"bid"}).sort("price",pymongo.DESCENDING)];
	asks = [json.dumps(ask, default=json_util.default) for ask in collection.find({"type":"ask"}).sort("price",pymongo.ASCENDING)];

bid_data= {}
for b in bids:
	p = int(float(b.split(',')[3][10:]))
	if p % 2 != 0:
		p=p-1
	bid_data[p]=0 
for b in bids:
	p = int(float(b.split(',')[3][10:]))
	if p % 2 != 0:
		p=p-1
#	if p==226:
#		print b
	bid_data[p]=bid_data[p]+float(b.split(',')[4][11:])

ask_data= {}
for a in asks:
	p = int(float(a.split(',')[3][10:]))
	if p % 2 == 0:
		p=p+1
	p=p+1
	ask_data[p]=0 
for a in asks:
	p = int(float(a.split(',')[3][10:]))
	if p % 2 == 0:
		p=p+1
	p=p+1
	ask_data[p]=ask_data[p]+float(a.split(',')[4][11:])

bid_series=pd.Series(bid_data).sort_index(ascending=False)
ask_series=pd.Series(ask_data).sort_index(ascending=False)


print ask_series[len(ask_series)-20:len(ask_series)]
print bid_series[0:20]

stop = timeit.default_timer()

print stop - start
