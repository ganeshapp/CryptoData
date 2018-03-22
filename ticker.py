import json, requests
import datetime
import time
from git import Repo

# Get Load Date
sysdate = datetime.datetime.fromtimestamp(int(time.time())).strftime('%Y-%m-%d %H:%M:%S')

# All the Files
file_ticker = open('~/CryptoData/ticker.csv', 'a')

# Get ticker data from coin market cap
api = 'https://api.coinmarketcap.com/v1/ticker/?limit=0'
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
    available_supply = float(x["available_supply"] or 0)
    total_supply = float(x["total_supply"] or 1)
    max_supply = float(x["max_supply"] or 1)
    p_change_hour = float(x["percent_change_1h"] or 0.0) / 100
    p_change_day = float(x["percent_change_24h"] or 0.0) / 100
    p_change_week = float(x["percent_change_7d"] or 0.0) / 100
    last_updated = datetime.datetime.fromtimestamp(int(x["last_updated"] or time.time())).strftime('%Y-%m-%d %H:%M:%S')
    row_ticker = [id, name, symbol, rank, price, day_volume, market_cap, available_supply, total_supply, max_supply, p_change_hour, p_change_day, p_change_week, last_updated,
                  sysdate]
    file_ticker.write(','.join(str(e) for e in row_ticker) + '\n')
    # Historical Data
file_ticker.close()
# github push
repo_dir = '~/CryptoData/'
repo = Repo(repo_dir)
file_list = [
    '~/CryptoData/ticker.csv'
]
commit_message = 'Update ticker file'
repo.index.add(file_list)
repo.index.commit(commit_message)
origin = repo.remote('origin')
origin.push()