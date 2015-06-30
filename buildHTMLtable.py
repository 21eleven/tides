import sys
import time
import requests
import json
import pandas as pd
import subprocess

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

#orders_df.index = orders_df['reqtimestamp']
print orders_df["amount","price"][5:11]
'''records_j = orders_df.to_csv()
print records_j

csv_file = open("/tmp/orders.csv", "w")
csv_file.write("index"+records_j) 
csv_file.close()
#con.tides.books.insert(records_j)
#mongoimport -d tides -c books --type csv --file /tmp/orders.csv --headerline
mongoimportCMD = subprocess.call("mongoimport -d tides -c books --type csv --file /tmp/orders.csv --headerline", shell=True)
print mongoimportCMD
subprocess.call("rm /tmp/orders.csv", shell=True)
#db.books.find({reqtimestamp : {$lt:1422935380, $gt:1422935380-500}, price : {$gte: 240, $lt: 245}})'''
