from SmartApi import SmartConnect
from pyotp import TOTP
import urllib
import os
from key import *
import json
import pandas as pd
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

obj = SmartConnect(api_key=apikey)
data = obj.generateSession(userid,passwd,TOTP(otp).now())

url = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"
response = urllib.request.urlopen(url)
list = json.loads(response.read())

def token_lookup(ticker,list, exchange="NSE"):
    for scrip in list:
        if scrip['name'] == ticker and scrip['exch_seg'] == exchange and scrip['symbol'].split('-')[-1] == 'EQ':
            return scrip['token']
        
def symbol_lookup(token,list, exchange="NSE"):
    for scrip in list:
        if scrip['token'] == token and scrip['exch_seg'] == exchange and scrip['symbol'].split('-')[-1] == 'EQ':
            return scrip['name']
        
ticker = input("Enter any scrip symbol to find the token:  ").upper() 
symbol = input("Enter any scrip token to find the symbol:  ").upper()

def hist_data(ticker,st_date,end_date,interval,list,exchange='NSE'):
    params = {
        "exchange": exchange,
        "symboltoken":token_lookup(ticker,list),
        "interval": interval,
        "fromdate": st_date,
        "todate" :end_date
    }
    hist_data = obj.getCandleData(params)
    df_data = pd.DataFrame(hist_data['data'],columns=['date','open','high','low','close','volume'])
    df_data.set_index('date',inplace=True)
    return df_data

stock_data = hist_data(ticker,"2023-01-01 09:15","2023-06-30 15:30","ONE_HOUR",list)
print(stock_data)


        
print(token_lookup(ticker,list))
print(symbol_lookup(symbol,list))