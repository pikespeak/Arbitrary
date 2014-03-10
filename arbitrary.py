#import the lib that connects to URLs
import urllib.request
import json
#this is usually done by default, locale settings
import locale
locale.setlocale(locale.LC_ALL, '')
#this will allow the app to run automatically
import threading
import subprocess
#provide timestamps for output
import datetime

#set the default CAD value to 100 for easy calculations
amount = 100


def arbitrage():

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

  #finding an exchange in the bitcoincharts API: create a list where 0 = bid, 1 = ask
  def exchange(symbol):
    for item in bc:
      if item.get("symbol") == symbol:
        bid = item.get("bid")
        ask = item.get("ask")
        return bid, ask

  #Virtex market data
  virtex_bid = exchange("virtexCAD")[0]
  virtex_ask = exchange("virtexCAD")[1]
  virtex_cmsn = 0.015 #commission

  #Bitstamp market data
  bs_bid = exchange("bitstampUSD")[0]
  bs_ask = exchange("bitstampUSD")[1]
  bs_cmsn = 0.005 #commission

  #BTC-e market data
  btce_bid = exchange("btceUSD")[0]
  btce_ask = exchange("btceUSD")[1]
  btce_cmsn = 0.002 #commission

  #Quadriga CX market data
  qcx_bid = float(qcx["btc_cad"]["buy"])
  qcx_ask = float(qcx["btc_cad"]["sell"])
  qcx_cmsn = 0 #commission

  #Vault of Satoshi market data
  vs_bid = float(vs["data"]["bids"][0]["price"]["value"])
  vs_ask = float(vs["data"]["asks"][0]["price"]["value"])
  vs_cmsn = 0.01 #commission

  
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

  #BTC-e -> Bitstamp
  buy_btce = (amount - amount * btce_cmsn) / btce_ask
  sell_bs = (buy_btce - buy_btce * bs_cmsn) * bs_bid
  bbs_pl = sell_bs - amount

  #BTC-e -> Bitstamp
  buy_bs = (amount - amount * bs_cmsn) / bs_ask
  sell_btce = (buy_bs - buy_bs * btce_cmsn) * btce_bid
  bsb_pl = sell_btce - amount

  #show timestamps
  time = datetime.datetime.now()
  
  #print results
  print("\n", "* * * * * * * * * * * * * *", "\n", time, "\n")

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

  print("BTC-e -> Bitstamp", "\n",
      "Profit / Loss:", bbs_pl, "\n")

  print("Bitstamp -> BTC-e", "\n",
      "Profit / Loss:", bsb_pl, "\n")

  threading.Timer(300, arbitrage).start()


arbitrage()



