from bs4 import BeautifulSoup
import requests
import time
import numpy as np
import pandas as pd
from pymongo import MongoClient
import urllib.parse

client = MongoClient('localhost', 27017)
db = client.largest_btc
notebook = db.notebook

username = urllib.parse.quote_plus('mongod')
password = urllib.parse.quote_plus('root123')
client = MongoClient('mongodb://%s:%s@127.0.0.1' % (username, password))

def btcScraper():
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


    Data = pd.DataFrame(list(zip(hashList, timeList, BTCamountList, amount)),
                        columns=["Hash","Time","Amount (BTC)","Amount (USD)"])

    highest = Data.sort_values(by=['Amount (USD)'], ascending=False).head(1).iloc[0]



    return highest.to_dict()


while True:
    obs = btcScraper()
    notebook.insert_one(obs)
    time.sleep(60)
