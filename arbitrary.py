#import the lib that connects to URLs
import urllib.request
import json
#this is usually done by default, locale settings
import locale
locale.setlocale(locale.LC_ALL, '')
#this will allow the app to run automatically
import threading
import subprocess

#opening and assigning a bitcoincharts URL to a variable
bc_api = urllib.request.urlopen("http://api.bitcoincharts.com/v1/markets.json")

"""In Python 3, binary data, such as the raw response of a http request,
is stored in bytes objects. json/simplejson expects strings. The solution is
to decode the bytes data to string data with the appropriate encoding, which
you can find in the header"""

#encoding and decoding
encoding = bc_api.headers.get_content_charset('utf-8')
bc = json.loads(bc_api.read().decode(encoding))

#finding an exchange: create a list where 0 = exchange name, 1 = bid, 2 = ask
def exchange(symbol):
  for item in bc:
    if item.get("symbol") == symbol:
      name = item.get("symbol")
      bid = item.get("bid")
      ask = item.get("ask")
      return name, bid, ask
    
  
#Virtex data
virtex_bid = exchange("virtexCAD")[1]
virtex_ask = exchange("virtexCAD")[2]
virtex_commission = 0.015

print("Virtex BID is", virtex_bid, "\n Virtex ASK is", virtex_ask)
#def arbitrage():
  #restart function in x seconds
#	threading.Timer(300, arbitrage).start()


#arbitrage()



