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

#same for Quadriga CX
qcx_api = urllib.request.urlopen("http://api.quadrigacx.com/public/info")

"""In Python 3, binary data, such as the raw response of a http request,
is stored in bytes objects. json/simplejson expects strings. The solution is
to decode the bytes data to string data with the appropriate encoding"""

#encoding and decoding
encoding_bc = bc_api.headers.get_content_charset('utf-8')
bc = json.loads(bc_api.read().decode(encoding_bc))

encoding_qcx = qcx_api.headers.get_content_charset('utf-8')
qcx = json.loads(qcx_api.read().decode(encoding_qcx))

#finding an exchange in the bitcoincharts API: create a list where 0 = bid, 1 = ask
def exchange(symbol):
  for item in bc:
    if item.get("symbol") == symbol:
      bid = item.get("bid")
      ask = item.get("ask")
      return bid, ask

#set the default CAD value to 100 for easy calculations
amount = 100

#Virtex data
virtex_bid = exchange("virtexCAD")[0]
virtex_ask = exchange("virtexCAD")[1]
virtex_cmsn = amount * 0.015 #commission

#Quadriga CX market data
qcx_bid = float(qcx["btc_cad"]["sell"])
qcx_ask = float(qcx["btc_cad"]["buy"])
qcx_cmsn = 0 #commission

#profit / loss calculator
#Virtex -> Quadriga CX
buy_virtex = (amount - virtex_cmsn) / virtex_bid
sell_qcx = buy_virtex * qcx_ask
vq_pl = sell_qcx - amount

#Quadriga CX -> Virtex
buy_qcx = (amount - qcx_cmsn) / qcx_bid
sell_virtex = buy_qcx * virtex_ask
qv_pl = sell_virtex - amount


def arbitrage():
  print("Virtex -> Quadriga CX", "\n",
      "Profit / Loss:", vq_pl)

  print("Quadriga CX -> Virtex", "\n",
      "Profit / Loss:", qv_pl)

  #restart function in x seconds
  #threading.Timer(15, arbitrage).start()


arbitrage()



