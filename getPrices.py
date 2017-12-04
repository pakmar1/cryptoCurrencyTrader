import time
import pymysql as sql
from   datetime import datetime
import requests as url

DEBUG = 1
FETCH_FREQUENCY = 2
pattern         = '%Y-%m-%d %H:%M:%S'
COMPUTE_HOURLY  = 0

LTC_URL = "https://api.coinmarketcap.com/v1/ticker/litecoin/"
ETH_URL = "https://api.coinmarketcap.com/v1/ticker/ethereum/"
BTC_URL = "https://api.coinmarketcap.com/v1/ticker/bitcoin/"

btc_price = ltc_price = eth_price = 0
btc_table = "bitcoindata"
ltc_table = "litecoindata"
eth_table = "ethereumdata"

currency_code = 'USD'  # can also use EUR, CAD, etc.

def calculatePortfolioValue(cursor, timeStamp, btc_price, ltc_price, eth_price):

	getUserIds = "SELECT userid FROM user;"
	cursor.execute(getUserIds)
	userIds = [x[0] for x in cursor.fetchall()]
	
	for uId in userIds:
		portfolio = "SELECT portfolioid, amount, bitcoin, ethereum, litecoin from portfolio where userid = uid;"
		cursor.execute(getWalletAmt)
		pId, vAmnt, bcoin, ecoin, lcoin = cursor.fetchall()
		bValue = bcoin*btc_price
		eValue = ecoin*eth_price
		lValue = lcoin*ltc_price
		portfolioValue = vAmnt + bValue + lValue + eValue

		insertHourly = "INSERT INTO portfolio_hourly (portfolioid, userid, timestmp, bitcoin, ethereum, litecoin, amount) \
		                VALUES (%d, %d, %d, %d, %d, %d, %d) " % (pId, uId, timeStamp, bValue, eValue, lValue, portfolioValue)
		cursor.execute(insertHourly)

while(1):

	time.sleep(FETCH_FREQUENCY)
	db = sql.connect(host   = "127.0.0.1",
		 			 user   = "root",
					 passwd = "admin",
					 db     = "cryptxmaster"
	)

	cursor = db.cursor()
	
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

		query = "INSERT INTO %s (timestmp, litecoinvalue) VALUES(%d, %d);" % (ltc_table, timeStamp, float(ltc_price))
		cursor.execute(query)
		if(DEBUG):
			print("Inserted LTC price")

		query = "INSERT INTO %s (timestmp, ethereumvalue) VALUES(%d, %d);" % (eth_table, timeStamp, float(eth_price))
		cursor.execute(query)
		if(DEBUG):
			print("Inserted ETH price")

		if(not COMPUTE_HOURLY % 60):
			calculatePortfolioValue(cursor, timeStamp, btc_price, ltc_price, eth_price)
			COMPUTE_HOURLY = 0

	except:
		if(DEBUG):		
			print("ROLLBACK!")
		db.rollback()

	db.commit()
	if(DEBUG):
		print("DB Commit")
	db.close()
	if(DEBUG):
		print("Connection closed.")

	COMPUTE_HOURLY += 1
