import sqlite3
import requests
import json
from enum import Enum
import time
import calendar
import hmac
from typing import Dict
import hashlib
import time
import requests
import json


base_url ="https://api2.binance.com"
api_key="PutYourApiKeyHere"
secret_key="PutYourSecretKeyHere"

def getTokenAvaible():
    r = requests.get(base_url + "/api/v3/ping")
    if (r.status_code == 200):
        print("api2 connecté")
    r = requests.get(base_url + "/api/v3/exchangeInfo")
    if (r.status_code == 200):
        print("api2 echange info connecté")
        print(type(r.json()["symbols"]))
        listeTokenAvaible = []
        for symbol in r.json()["symbols"]:
            if symbol["baseAsset"] not in listeTokenAvaible:
                listeTokenAvaible.append(symbol["baseAsset"])
    return listeTokenAvaible

def getDepth(symbol,ask,bid): ## boolean pour choisir ce que l'on veut
    r=requests.get(base_url + "/api/v3/depth?symbol=" + symbol +"&limit=1")
    print(r.json())
    if(ask==True and bid==True):
        print("ask : " +str(r.json()['asks'][0][0]))
        print("bid : " + str(r.json()['bids'][0][0]))
        return(r.json()['asks'][0][0],r.json()['bids'][0][0])
    elif(ask != True):
        print("bid : " + str(r.json()['bids'][0][0]))
        return(r.json()['bids'][0][0])
    else:
        print("ask : " + str(r.json()['asks'][0][0]))
        return(r.json()['asks'][0][0])

def getOrderBook(symbol,limite):
    r=requests.get(base_url + "/api/v3/depth?symbol=" + symbol +"&limit=" + str(limite))
    return (r.json()['asks'],r.json()['bids'])

class PeriodeInterval(Enum):
    minutes = { 1 :'1m',3:'3m',5:'5m',15:'15m',30:'30m'}
    heures = { 1 : '1h',2: '2h',4: '4h',6: '6h',8: '8h',12: '12h'}
    days ={1 : '1j',3:'3j'}
    semaine = '1s'
    mois ='1M'

def insertCandlesbdd(a,connection):
    cursor = connection.cursor()
    requete = f"insert into candles (openTime ,open , high ,low , close ,volume ,closeTime) values ({a[0]},{a[1]},{a[2]},{a[3]},{a[4]},{a[5]},{a[6]})"
    cursor.execute(requete)
    connection.commit()


def refresreshDatCandle(symbol,Periode):
    r = requests.get(base_url+ "/api/v3/klines?symbol=" + symbol +"&interval=" +Periode)
    connection = sqlite3.connect('ApiBinance.db')
    for a in r.json():
        insertCandlesbdd(a,connection)
    connection.close()

def insertTradesbdd(a,connection):
    cursor = connection.cursor()
    requete = f"insert into trades (idTrade ,price , qty ,quoteqty , time ,isBuyerMaker ,isbestMatch ) values ({a['id']},{a['price']},{a['qty']},{a['quoteQty']},{a['time']},{a['isBuyerMaker']},{a['isBestMatch']})"
    cursor.execute(requete)
    connection.commit()

def refreshData(symbol):
    headers = {
        'Content-Type': 'application/json',
        'X-MBX-APIKEY': api_key
    }
    r = requests.get(base_url + "/api/v3/historicalTrades?symbol=" + symbol,headers=headers)
    connection = sqlite3.connect('ApiBinance.db')
    print(r.json()[0])
    for a in r.json():
        insertTradesbdd(a,connection)
    connection.close()

def makeOrder(symbol,side,type,timeInForce,quantity,price,):
    secret = secret_key
    timestamp = requests.get(base_url + "/api/v3/time").json()["serverTime"]
    query_string = "symbol="+symbol+"&side="+side+"&type="+type +"&timeInForce="+timeInForce+"&quantity="+quantity+ "&price="+price+ "&timestamp="+str(timestamp)
    signature = hmac.new(secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
    headers = {
        'Content-Type': 'application/json',
        'X-MBX-APIKEY': api_key
    }
    r = requests.post(base_url + "/api/v3/order?"
                      + "symbol="+symbol
                      + "&side="+side
                      + "&type="+type
                      + "&timeInForce="+timeInForce
                      + "&quantity="+quantity
                      + "&price="+price
                      + "&timestamp="+str(timestamp)
                      + "&signature="+signature,headers=headers)
    print(r.json())
    return r.json()

def cancelOrder(symbol,orderId):
    secret = secret_key
    timestamp = requests.get(base_url + "/api/v3/time").json()["serverTime"]
    query_string = "symbol="+symbol+"&orderId="+orderId+"&timestamp="+str(timestamp)
    signature = hmac.new(secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
    headers = {
        'Content-Type': 'application/json',
        'X-MBX-APIKEY': api_key
    }
    r=requests.delete(base_url+"/api/v3/order?symbol="+symbol+"&orderId="+orderId+"&timestamp="+str(timestamp)+"&signature="+signature,headers=headers)
    print(r.text)



if __name__ == '__main__':
    ##print(getTokenAvaible())
    ##print(getDepth('ETHBTC',False,True))
    ##print(getOrderBook('ETHBTC', 100))
    ##refresreshDatCandle('MATICUSDT', PeriodeInterval['minutes'].value[1])
    #OrderId = makeOrder('MATICUSDT','SELL','LIMIT','GTC','10','5')['orderId']
    #cancelOrder('MATICUSDT',str(OrderId))
    #refreshData('MATICUSDT')
    pass







