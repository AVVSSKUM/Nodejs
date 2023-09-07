from SmartApi import SmartConnect
from pyotp import TOTP
import urllib
import os
from key import *
import json
import pandas as pd
import datetime as dt
import time

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
symbol = input("Enter any scrip token to find the symbol:  ")

def hist_data_extended(ticker,duration,interval,list,exchange='NSE'):
    st_date = dt.date.today()-dt.timedelta(duration)

    end_date= dt.date.today()
    st_date = dt.datetime(st_date.year, st_date.month,st_date.day,9,15)
    end_date = dt.datetime(end_date.year,end_date.month, end_date.day)
    df_data = pd.DataFrame(columns=['date','open','high','low','close','volume'])
    while st_date < end_date:
        time.sleep(0.5)
        params = {
            "exchange": exchange,
            "symboltoken":token_lookup(ticker,list),
            "interval": interval,
            "fromdate": (st_date).strftime('%Y-%m-%d %H:%M'),
            "todate" : (end_date).strftime('%Y-%m-%d %H:%M')
        }
        hist_data = obj.getCandleData(params)
        temp = pd.DataFrame(hist_data['data'],columns=['date','open','high','low','close','volume'])
        #df_data = temp.append(df_data,ignore_index=True)
        df_data = pd.concat([temp,df_data])
        end_date = dt.datetime.strptime(temp['date'].iloc[0][:16],'%Y-%m-%dT%H:%M')
        if len(temp)<=1:
            break
        df_data.set_index('date',inplace=True)
        df_data.index=pd.to_datetime(df_data.index)
        df_data.index = df_data.index.tz_localize(None)
        df_data.drop_duplicates(keep="first", inplace=True)
        return df_data

stock_data = hist_data_extended(ticker,300,"ONE_HOUR",list)
print(stock_data)