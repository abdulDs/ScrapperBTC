from bs4 import BeautifulSoup
import requests
import time
import numpy as np
import pandas as pd
from pymongo import MongoClient
import urllib.parse
import redis
import pyarrow as pa

redis = redis.Redis(host='localhost')
# this program scrapes the data from the website 
def scrapes_BTC_Data():
    r = requests.get('https://www.blockchain.com/btc/unconfirmed-transactions')
    soup = BeautifulSoup(r.text, 'lxml')

    hashList=[]
    timeList=[]
    BTCamountList=[]
    USDamountList=[]

    a = soup.findAll('div', {"class":"sc-1g6z4xm-0 arCxa"})
    for element in a:
        hashList.append(element.findAll(['span','a'])[1].text)
        timeList.append(element.findAll(['span','a',])[3].text)
        BTCamountList.append(element.findAll(['span','a'])[5].text)
        USDamountList.append(element.findAll(['span','a',])[7].text)

    stripedList = [s.strip('$')for s in USDamountList]
    amount = [float(s.replace(',','')) for s in stripedList]

    return pd.DataFrame(list (zip(hashList,timeList,BTCamountList,amount)),
                        columns = ["Hash", "Time", "Amount (BTC)", "Amount (USD)"])

## cache the data
def cachingToRedis():
    ## caching the data into redis meomory and delet it after 60 sec
    context = pa.default_serialization_context()
    redis.set('key',context.serialize(scrapes_BTC_Data()).to_buffer().to_pybytes())
    redis.expire('key',60)
    return context

#retrun the data with it's highest value
def topFromredis():
    return cachingToRedis().deserialize(redis.get('key')).sort_values(by=['Amount (USD)'], ascending=False).head(1).iloc[0].to_dict()



client = MongoClient('localhost', 27017)
db = client.largest_btc
notebook = db.notebook
# insert the top value in our mongodb
def storeToMongodb():
    notebook.insert_one(topFromredis())



def cachingMehanism():
    cachingToRedis()
    topFromredis()
    storeToMongodb()
    
while True:
    scrapes_BTC_Data()
    cachingMehanism()
    time.sleep(61)
