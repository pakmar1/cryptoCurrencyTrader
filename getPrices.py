# import MySQLdb as sql 
import time
from datetime import datetime
import requests as url

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

# db = sql.connect(host   = "127.0.0.1",
# 	 			 user   = "root",
# 				 passwd = "admin",
# 				 db     = "cryptxmaster"
# )

# cursor = db.cursor()

for _ in range(50):
	time.sleep(FETCH_FREQUENCY)
	
	t = str(datetime.now())
	t = t.split('.')[0]
	
	epoch  = int(time.mktime(time.strptime(t, pattern)))
	
	btc_price = url.get(BTC_URL).json()[0]['price_usd']
	print('BTC price at %s : %s %s' % (epoch, btc_price, currency_code))
	
	ltc_price = url.get(LTC_URL).json()[0]['price_usd']
	print('LTC price at %s : %s %s' % (epoch, ltc_price, currency_code))

	eth_price = url.get(ETH_URL).json()[0]['price_usd']
	print('ETH price at %s : %s %s' % (epoch, eth_price, currency_code))

	timeStamp = epoch
	# btcPrice  = float(price.amount)

	# query = "INSERT INTO bitcoindata VALUES(%d, %d)" % (timeStamp, btcPrice)
	# queryStatus = cursor.execute(query)
	# print(queryStatus)

# db.commit()
# db.close()
