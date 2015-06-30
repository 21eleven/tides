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
from pymongo import MongoClient
from bson import json_util
import optparse


client = MongoClient('localhost', 27017)
db = client['tides']


collection = db.books
current = Popen(['date','+%s'], stdout=PIPE).communicate()
current_int = int((''.join(map(str,current))[:10]))
time = current_int 
print time
#orders = [json.dumps(bid, default=json_util.default) for bid in collection.find({"reqtimestamp" : {"$lt":time-432000}}).sort("price",pymongo.DESCENDING)];
#orders = collection.find({"reqtimestamp" : {"$lt":time-432000}}).count()
collection.remove({"reqtimestamp" : {"$lt":time-432000}})
#print orders

stop = timeit.default_timer()

print stop - start
