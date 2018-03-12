from lxml import html
import requests
import numpy as np
import json, requests
import datetime
import time
from git import Repo

# ToDO get all the current data of the coins
# TODO get all the markets the coin is in
# TODO get all the Historical Data
# TODO make it into csv file
# TODO figure a way to upload the CSV file to Kaggle
#

# Get Load Date
sysdate = datetime.datetime.fromtimestamp(int(time.time())).strftime('%Y-%m-%d %H:%M:%S')

# All the Files
file_ticker = open('ticker.csv', 'w')
file_historical = open('historical_price.csv', 'w')
file_exchange= open('exchange.csv', 'w')

# All the headers
header_ticker = ['id','name','symbol','rank','price','day_volume','market_cap','p_day_vol','available_supply','total_supply','p_tot_supply','max_supply','p_max_supply','p_change_hour','p_change_day','p_change_week','last_updated','load_date']
header_historical = ['id','date','open','high','low','close','volume','market_cap']
header_exchange = ['id','exchange_name','exchange_pair','volume(24h)','price','volume(%)']

# Write headers into files
file_ticker.write(','.join(str(e) for e in header_ticker)+'\n')
file_historical.write(','.join(str(e) for e in header_historical)+'\n')
file_exchange.write(','.join(str(e) for e in header_exchange)+'\n')

# Get ticker data from coin market cap
api = 'https://api.coinmarketcap.com/v1/ticker/?limit=200'
row_count = 0
resp = requests.get(url=api)
data = json.loads(resp.text)

for x in data:
    # Ticker Data
    id = x["id"]
    name = x["name"]
    symbol = x["symbol"]
    rank = int(x["rank"] or 0)
    price = float(x["price_usd"] or 0)
    day_volume = float(x["24h_volume_usd"] or 0)
    market_cap = float(x["market_cap_usd"] or 1)
    p_day_vol = day_volume/market_cap
    available_supply = float(x["available_supply"] or 0)
    total_supply = float(x["total_supply"] or 1)
    max_supply = float(x["max_supply"] or 1)
    p_tot_supply = available_supply/total_supply
    if p_tot_supply > 1:
        p_tot_supply = 0
    p_max_supply = available_supply/max_supply
    if p_max_supply > 1:
        p_max_supply = 0
    p_change_hour = float(x["percent_change_1h"] or 0.0)/100
    p_change_day = float(x["percent_change_24h"] or 0.0)/100
    p_change_week = float(x["percent_change_7d"] or 0.0)/100
    last_updated = datetime.datetime.fromtimestamp(int(x["last_updated"] or time.time())).strftime('%Y-%m-%d %H:%M:%S')
    row_ticker = [id, name, symbol, rank, price, day_volume, market_cap, p_day_vol, available_supply, total_supply, p_tot_supply, max_supply, p_max_supply, p_change_hour, p_change_day, p_change_week, last_updated, sysdate]
    file_ticker.write(','.join(str(e) for e in row_ticker) + '\n')
    print('id', id)
    # Historical Data
    historical_data_url = 'https://coinmarketcap.com/currencies/'+id+'/historical-data/?start=20170101&end='+datetime.datetime.fromtimestamp(int(time.time())).strftime('%Y%m%d')
    page = requests.get(historical_data_url)
    tree = html.fromstring(page.content)
    historical_data = tree.xpath('//td/text()')
    historical_data_table = np.reshape(np.array(historical_data), (-1, 7))
    for data_historical in historical_data_table:
        date = datetime.datetime.strptime(data_historical[0], "%b %d, %Y").date()
        row_history = [id, date.strftime('%Y-%m-%d'), float(data_historical[1].replace('-','').replace(',','') or 0.0),float(data_historical[2].replace('-','').replace(',','') or 0.0), float(data_historical[3].replace('-','').replace(',','') or 0.0),float(data_historical[4].replace('-','').replace(',','') or 0.0),int(data_historical[5].replace('-','').replace(',','') or 0),int(data_historical[6].replace('-','').replace(',','') or 0)]
        file_historical.write(','.join(str(e) for e in row_history) + '\n')

    # Exchange Data
    exchange_data_url = 'https://coinmarketcap.com/currencies/' + id + '/#markets'
    exchange_page = requests.get(exchange_data_url)
    exchange_tree = html.fromstring(exchange_page.content)
    exchange_data = exchange_tree.xpath('//td/a/text()|//td/span/text()')
    exchange_data_table = np.reshape(np.array(exchange_data), (-1, 5))
    for data_exchange in exchange_data_table:
        row_exchange = [id, data_exchange[0], data_exchange[1], data_exchange[2].replace("\n",'').replace('$','').replace(',',''),data_exchange[3].replace("\n",'').replace(',', '').replace('$',''),float(data_exchange[4] or 0.0)/100.0 ]
        file_exchange.write(','.join(str(e) for e in row_exchange) + '\n')


print('Completed')
file_ticker.close()
file_historical.close()
file_exchange.close()