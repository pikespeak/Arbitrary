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
#ct_api = urllib.request.urlopen("https://www.cointrader.net/trader/api/orderbook?currency=USD")

#same for Vault of Satoshi
vs_api = urllib.request.urlopen("https://api.vaultofsatoshi.com/public/orderbook?order_currency=BTC&payment_currency=CAD")

"""In Python 3, binary data, such as the raw response of a http request,
is stored in bytes objects. json/simplejson expects strings. The solution is
to decode the bytes data to string data with the appropriate encoding"""

#encoding and decoding
encoding_bc = bc_api.headers.get_content_charset('utf-8')
bc = json.loads(bc_api.read().decode(encoding_bc))

encoding_qcx = qcx_api.headers.get_content_charset('utf-8')
qcx = json.loads(qcx_api.read().decode(encoding_qcx))

encoding_vs = vs_api.headers.get_content_charset('utf-8')
vs = json.loads(vs_api.read().decode(encoding_vs))

"""
encoding_ct = ct_api.headers.get_content_charset('utf-8')
ct = json.loads(ct_api.read().decode(encoding_ct))
"""

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
qcx_bid = float(qcx["btc_cad"]["buy"])
qcx_ask = float(qcx["btc_cad"]["sell"])
qcx_cmsn = 0 #commission

#Vault of Satoshi market data
vs_bid = float(vs["data"]["bids"][0]["price"]["value"])
vs_ask = float(vs["data"]["asks"][0]["price"]["value"])
vs_cmsn = 0.01 #commission


"""
#Cointrader market data
ct_bid = float(ct["bids"][len(ct["bids"])-1][0])
ct_ask = float(ct["asks"][len(ct["asks"])-1][0])
ct_cmsn = 0.005 #commission
"""

#profit / loss calculator. formula: buy: (amount - commission) / ask. sell: (amount - commission) * bid
#Virtex -> Quadriga CX
buy_virtex = (amount - amount * virtex_cmsn) / virtex_ask
sell_qcx = (buy_virtex - buy_virtex * qcx_cmsn) * qcx_bid
vq_pl = sell_qcx - amount

#Quadriga CX -> Virtex
buy_qcx = (amount - amount * qcx_cmsn) / qcx_ask
sell_virtex = (buy_qcx - buy_qcx * virtex_cmsn) * virtex_bid
qv_pl = sell_virtex - amount

#Virtex -> Vault of Satoshi
buy_virtex = (amount - amount * virtex_cmsn) / virtex_ask
sell_vs = (buy_virtex - buy_virtex * vs_cmsn) * vs_bid
vvs_pl = sell_vs - amount

#Vault of Satoshi -> Virtex
buy_vs = (amount - amount * vs_cmsn) / vs_ask
sell_virtex = (buy_vs - buy_vs * virtex_cmsn) * virtex_bid
vsv_pl = sell_virtex - amount

#Quadriga CX -> Vault of Satoshi
buy_qcx = (amount - amount * qcx_cmsn) / qcx_ask
sell_vs = (buy_qcx - buy_qcx * vs_cmsn) * vs_bid
qvs_pl = sell_vs - amount

#Vault of Satoshi -> Quadriga CX
buy_vs = (amount - amount * vs_cmsn) / vs_ask
sell_qcx = (buy_vs - buy_vs * qcx_cmsn) * qcx_bid
vsq_pl = sell_qcx - amount


"""
#Cointrader (USD) -> Bitstamp (USD)
buy_ct = (amount - amount * ct_cmsn) / ct_bid
sell_bs = (buy_ct - buy_ct * bs_cmsn) * bs_ask
cb_pl = sell_bs - amount

#Bitstamp (USD) -> Cointrader (USD)
buy_bs = (amount - amount * bs_cmsn) / bs_bid
sell_ct = (buy_bs - buy_bs * ct_cmsn) * ct_ask
bc_pl = sell_ct - amount
"""

def arbitrage():
  print("Virtex -> Quadriga CX", "\n",
      "Profit / Loss:", vq_pl, "\n")

  print("Quadriga CX -> Virtex", "\n",
      "Profit / Loss:", qv_pl, "\n")

  print("Virtex -> Vault of Satoshi", "\n",
      "Profit / Loss:", vvs_pl, "\n")
  
  print("Vault of Satoshi -> Virtex", "\n",
      "Profit / Loss:", vsv_pl, "\n")
  
  print("Quadriga CX -> Vault of Satoshi", "\n",
      "Profit / Loss:", qvs_pl, "\n")
  
  print("Vault of Satoshi -> Quadriga CX", "\n",
      "Profit / Loss:", vsq_pl, "\n")

  #restart function in x seconds
  threading.Timer(180, arbitrage).start()


"""
  print("Cointrader (USD) -> Bitstamp (USD)", "\n",
      "Profit / Loss:", cb_pl, "\n")
  
  print("Bitstamp (USD) -> Cointrader (USD)", "\n",
      "Profit / Loss:", bc_pl, "\n")
"""


arbitrage()



