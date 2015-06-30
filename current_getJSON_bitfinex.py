import sys
import time
import requests
import json
import pandas as pd
import subprocess
import pymongo
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
print client
db = client['tides']
db.currentbook.remove({})

currently = time.time()

r = requests.get('https://api.bitfinex.com/v1/book/btcusd')

bids_j = r.json()['bids']
asks_j = r.json()['asks']

bids_df = pd.DataFrame(bids_j)
asks_df = pd.DataFrame(asks_j)[::-1]


bids_df['type'] = 'bid'
asks_df['type'] = 'ask'

bids_df['reqtimestamp'] = currently
asks_df['reqtimestamp'] = currently

orders_df = asks_df.append(bids_df, ignore_index=True)

records_j = orders_df.to_csv()

csv_file = open("/tmp/current.csv", "w")
csv_file.write("index"+records_j) 
csv_file.close()

mongoimportCMD = subprocess.call("mongoimport -d tides -c currentbook --type csv --file /tmp/current.csv --headerline", shell=True)

subprocess.call("rm /tmp/current.csv", shell=True)

currentz=db.currentbook.find({"price" : {"$gte": 240, "$lt": 245}})
print currentz
