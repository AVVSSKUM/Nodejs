from SmartApi import SmartConnect
from pyotp import TOTP
import urllib
import os
from key import *
import json

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
        
print(token_lookup(ticker,list))
print(symbol_lookup(symbol,list))