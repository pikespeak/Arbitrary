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

#same for Cointrader
ct_api = urllib.request.urlopen("https://www.cointrader.net/trader/api/orderbook?currency=USD")


"""In Python 3, binary data, such as the raw response of a http request,
is stored in bytes objects. json/simplejson expects strings. The solution is
to decode the bytes data to string data with the appropriate encoding"""

#encoding and decoding
encoding_bc = bc_api.headers.get_content_charset('utf-8')
bc = json.loads(bc_api.read().decode(encoding_bc))

encoding_qcx = qcx_api.headers.get_content_charset('utf-8')
qcx = json.loads(qcx_api.read().decode(encoding_qcx))

encoding_ct = ct_api.headers.get_content_charset('utf-8')
ct = json.loads(ct_api.read().decode(encoding_ct))


#finding an exchange in the bitcoincharts API: create a list where 0 = bid, 1 = ask
def exchange(symbol):
  for item in bc:
    if item.get("symbol") == symbol:
      bid = item.get("bid")
      ask = item.get("ask")
      return bid, ask

#set the default CAD value to 100 for easy calculations
amount = 100

#Virtex market data
virtex_bid = exchange("virtexCAD")[0]
virtex_ask = exchange("virtexCAD")[1]
virtex_cmsn = 0.015 #commission

#Bitstamp data market
bs_bid = exchange("bitstampUSD")[0]
bs_ask = exchange("bitstampUSD")[1]
bs_cmsn = 0.002 #commission

#Quadriga CX market data
qcx_bid = float(qcx["btc_cad"]["sell"])
qcx_ask = float(qcx["btc_cad"]["buy"])
qcx_cmsn = 0 #commission

#Cointrader market data
ct_bid = float(ct["bids"][len(ct["bids"])-1][0])
ct_ask = float(ct["asks"][len(ct["asks"])-2][0])
ct_cmsn = 0.005 #commission

#profit / loss calculator
#Virtex -> Quadriga CX
buy_virtex = (amount - amount * virtex_cmsn) / virtex_bid
sell_qcx = buy_virtex * qcx_ask
vq_pl = sell_qcx - amount

#Quadriga CX -> Virtex
buy_qcx = (amount - amount * qcx_cmsn) / qcx_bid
sell_virtex = buy_qcx * virtex_ask
qv_pl = sell_virtex - amount

#Cointrader (USD) -> Bitstamp (USD)
buy_ct = (amount - amount * ct_cmsn) / ct_bid
sell_bs = (buy_ct - buy_ct * bs_cmsn) * bs_ask
cb_pl = sell_bs - amount

#Bitstamp (USD) -> Cointrader (USD)
buy_bs = (amount - amount * bs_cmsn) / bs_bid
sell_ct = (buy_bs - buy_bs * ct_cmsn) * ct_ask
bc_pl = sell_ct - amount

def arbitrage():
  print("Virtex -> Quadriga CX", "\n",
      "Profit / Loss:", vq_pl, "\n")

  print("Quadriga CX -> Virtex", "\n",
      "Profit / Loss:", qv_pl, "\n")

  print("Cointrader (USD) -> Bitstamp (USD)", "\n",
      "Profit / Loss:", cb_pl, "\n")
  
  print("Bitstamp (USD) -> Cointrader (USD)", "\n",
      "Profit / Loss:", bc_pl, "\n")

  #restart function in x seconds
  #threading.Timer(15, arbitrage).start()


arbitrage()



