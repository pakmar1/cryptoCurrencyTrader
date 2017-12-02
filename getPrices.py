import time
import pymysql as sql
from   datetime import datetime
import requests as url

DEBUG = 0
FETCH_FREQUENCY = 5
pattern         = '%Y-%m-%d %H:%M:%S'

LTC_URL = "https://api.coinmarketcap.com/v1/ticker/litecoin/"
ETH_URL = "https://api.coinmarketcap.com/v1/ticker/ethereum/"
BTC_URL = "https://api.coinmarketcap.com/v1/ticker/bitcoin/"

btc_price = ltc_price = eth_price = 0
btc_table = "bitcoindata"
ltc_table = "litecoindata"
eth_table = "ethereumdata"

currency_code = 'USD'  # can also use EUR, CAD, etc.

for _ in range(50):
	db = sql.connect(host   = "127.0.0.1",
		 			 user   = "root",
					 passwd = "admin",
					 db     = "cryptxmaster"
	)

	cursor = db.cursor()
	time.sleep(FETCH_FREQUENCY)
	
	# API calls to fetch the prices
	btc_price = url.get(BTC_URL).json()[0]['price_usd']
	ltc_price = url.get(LTC_URL).json()[0]['price_usd']
	eth_price = url.get(ETH_URL).json()[0]['price_usd']

	# Generate the epoch
	t = str(datetime.now())
	t = t.split('.')[0]
	timeStamp = int(time.mktime(time.strptime(t, pattern)))

	if(DEBUG):	
		print('BTC price at %s : %s %s' % (timeStamp, btc_price, currency_code))
		print('LTC price at %s : %s %s' % (timeStamp, ltc_price, currency_code))
		print('ETH price at %s : %s %s' % (timeStamp, eth_price, currency_code))

	# Insert the prices and timestamp into the tables
	try:	
		query = "INSERT INTO %s (timestmp, bitcoinvalue) VALUES(%d, %d);" % (btc_table, timeStamp, float(btc_price))
		cursor.execute(query)
		if(DEBUG):
			print("Inserted BTC price")	

		query = "INSERT INTO %s (timestmp, bitcoinvalue) VALUES(%d, %d);" % (ltc_table, timeStamp, float(ltc_price))
		cursor.execute(query)
		if(DEBUG):
			print("Inserted LTC price")

		query = "INSERT INTO %s (timestmp, bitcoinvalue) VALUES(%d, %d);" % (eth_table, timeStamp, float(eth_price))
		cursor.execute(query)
		if(DEBUG):
			print("Inserted ETH price")

	except:
		if(DEBUG):		
			print("ROLLBACK!")
		db.rollback()

	db.commit()
	db.close()
