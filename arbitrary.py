#import the lib that connects to URLs
import urllib.request
import json
#this is usually done by default, locale settings
import locale
locale.setlocale(locale.LC_ALL, '')
#this will allow the app to run automatically
import threading
import subprocess

#opening and assigning a URL to a variable
bc_api = urllib.request.urlopen("http://api.bitcoincharts.com/v1/markets.json")

"""In Python 3, binary data, such as the raw response of a http request,
is stored in bytes objects. json/simplejson expects strings. The solution is
to decode the bytes data to string data with the appropriate encoding, which
you can find in the header"""

#encoding and decoding
encoding = bc_api.headers.get_content_charset('utf-8')

#used json
bc_api_jsoned = json.loads(bc_api.read().decode(encoding))

"""
#Virtex data
virtex_data = json.dumps(bc_api_jsoned[11], indent=2)
virtex_ask = float(json.dumps(bc_api_jsoned[11]["ask"], indent=2))
virtex_bid = float(json.dumps(bc_api_jsoned[11]["bid"], indent=2))
virtex_cmsn = float(0.015)

#LibertyBit data
lybit_data = json.dumps(bc_api_jsoned[9], indent=2)
lybit_ask = float(json.dumps(bc_api_jsoned[9]["ask"], indent=2))
lybit_bid = float(json.dumps(bc_api_jsoned[9]["bid"], indent=2))
lybit_cmsn = float(0.005)

#Arbitrary trade profit/loss calculator
initial_cad = float(100)

#Virtex -> LibertyBit
virtex_lybit_final_cad = (((initial_cad - initial_cad * virtex_cmsn) / virtex_ask) - (((initial_cad - initial_cad * virtex_cmsn) / virtex_ask) * lybit_cmsn)) * lybit_bid
virtex_lybit_pl = virtex_lybit_final_cad - initial_cad

#LibertyBit -> Virtex
lybit_virtex_final_cad = (((initial_cad - initial_cad * lybit_cmsn) / lybit_ask) - (((initial_cad - initial_cad * lybit_cmsn) / lybit_ask) * virtex_cmsn)) * virtex_bid
lybit_virtex_pl = lybit_virtex_final_cad - initial_cad
"""

"""
def arbitrage():
	print("MtGOX ASK:", mtgox_ask, "CAD", "|", "MtGOX BID:", mtgox_bid, "CAD" "\n"
	"Virtex ASK:", virtex_ask, "CAD", "|", "Virtex BID:", virtex_bid, "CAD" "\n"
	"LibertyBit ASK:", lybit_ask, "CAD", "|", "LibertyBit BID:", lybit_bid, "CAD" "\n" "\n")
	
	print("Virtex (buy) -> LibertyBit (sell)" "\n"
	"Input:", initial_cad, "CAD", "|", "Output:", virtex_lybit_final_cad, "CAD", "|", "Profit/Loss:", virtex_lybit_pl, "CAD" "\n" "\n")
	
	print("LibertyBit (buy) -> Virtex (sell)" "\n"
	"Input:", initial_cad, "CAD", "|", "Output:", lybit_virtex_final_cad, "CAD", "|", "Profit/Loss:", lybit_virtex_pl, "CAD" "\n" "\n")
	
	print("MtGOX (buy) -> LibertyBit (sell)" "\n"
	"Input:", initial_cad, "CAD", "|", "Output:", mtgox_lybit_final_cad, "CAD", "|", "Profit/Loss:", mtgox_lybit_pl, "CAD" "\n" "\n")
	
	print("LibertyBit (buy) -> MtGOX (sell)" "\n"
	"Input:", initial_cad, "CAD", "|", "Output:", lybit_mtgox_final_cad, "CAD", "|", "Profit/Loss:", lybit_mtgox_pl, "CAD" "\n" "\n")
	
	print("MtGOX (buy) -> Virtex (sell)" "\n"
	"Input:", initial_cad, "CAD", "|", "Output:", mtgox_virtex_final_cad, "CAD", "|", "Profit/Loss:", mtgox_virtex_pl, "CAD" "\n" "\n")
	
	print("Virtex (buy) -> MtGOX (sell)" "\n"
	"Input:", initial_cad, "CAD", "|", "Output:", virtex_mtgox_final_cad, "CAD", "|", "Profit/Loss:", virtex_mtgox_pl, "CAD" "\n" "\n")
	
	print("------------------------------------------------------------------------------------", "\n" "\n")
	
	#play sound when Profit/Loss is positive - to be done after core features work
	
	#restart function in x seconds
	threading.Timer(300, arbitrage).start()
"""

def arbitrage():
  print("Hello, world!")

arbitrage()
		
