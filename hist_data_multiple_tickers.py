from SmartApi import SmartConnect
from pyotp import TOTP
import urllib
import os
from key import *
import json
import pandas as pd
import datetime as dt
pd.set_option('display.max_column', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_seq_items', None)
pd.set_option('display.max_colwidth', 500)
pd.set_option('expand_frame_repr', True)

obj = SmartConnect(api_key=apikey)
data = obj.generateSession(userid,passwd,TOTP(otp).now())

url = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"
response = urllib.request.urlopen(url)
list = json.loads(response.read())

tickers = ['ITC','BEL','INFY']

def token_lookup(ticker,list, exchange="NSE"):
    for scrip in list:
        if scrip['name'] == ticker and scrip['exch_seg'] == exchange and scrip['symbol'].split('-')[-1] == 'EQ':
            return scrip['token']
        
def symbol_lookup(token,list, exchange="NSE"):
    for scrip in list:
        if scrip['token'] == token and scrip['exch_seg'] == exchange and scrip['symbol'].split('-')[-1] == 'EQ':
            return scrip['name']
        
# ticker = input("Enter any scrip symbol to find the token:  ").upper() 
# symbol = input("Enter any scrip token to find the symbol:  ")

def hist_data(tickers,duration,interval,list,exchange='NSE'):
    hist_data_tickers = {}
    for ticker in tickers:
        params = {
            "exchange": exchange,
            "symboltoken": token_lookup(ticker,list),
            "interval": interval,
            "fromdate": (dt.date.today()-dt.timedelta(duration)).strftime('%Y-%m-%d %H:%M'),
            "todate" : dt.date.today().strftime('%Y-%m-%d %H:%M')
        }
        hist_data = obj.getCandleData(params)
        df_data = pd.DataFrame(hist_data['data'],columns=['date','open','high','low','close','volume'])
        df_data.set_index('date',inplace=True)
        df_data.index = pd.to_datetime(df_data.index)
        df_data.index = df_data.index.tz_localize(None)
        hist_data_tickers[ticker] =df_data
    return hist_data_tickers

stocks_data = hist_data(tickers,50,"ONE_HOUR",list)
print('\n'+stocks_data)


