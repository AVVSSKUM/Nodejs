# -*- coding: utf-8 -*-
"""
Angel One - Streaming tick level data websocket2.0

@author: Mayank Rasu (http://rasuquant.com/wp/)
"""

from SmartApi.smartWebSocketV2 import SmartWebSocketV2
from SmartApi import SmartConnect
import os
import urllib
import json
from pyotp import TOTP
from key import *



obj=SmartConnect(api_key=apikey)
data = obj.generateSession(userid,passwd,TOTP(otp).now())
feed_token = obj.getfeedToken()

instrument_url = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"
response = urllib.request.urlopen(instrument_url)
instrument_list = json.loads(response.read())

sws = SmartWebSocketV2(data["data"]["jwtToken"], apikey, userid, feed_token)


correlation_id = "stream_1" #any string value which will help identify the specific streaming in case of concurrent streaming
action = 1 #1 subscribe, 0 unsubscribe
mode = 3 #1 for LTP, 2 for Quote and 2 for SnapQuote

token_list = [{"exchangeType": 1, "tokens": ["26009"]}]


def on_data(wsapp, message):
    print("Ticks: {}".format(message))


def on_open(wsapp):
    print("on open")
    sws.subscribe(correlation_id, mode, token_list)


def on_error(wsapp, error):
    print(error)



# Assign the callbacks.
sws.on_open = on_open
sws.on_data = on_data
sws.on_error = on_error

sws.connect()