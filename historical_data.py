from lxml import html
import requests
import numpy as np
import json, requests
import datetime
from datetime import timedelta
import time
from git import Repo

# Get Load Date
sysdate = datetime.datetime.fromtimestamp(int(time.time())).strftime('%Y-%m-%d %H:%M:%S')

# All the Files
file_historical = open('historical_price.csv', 'a')

# Get ticker data from coin market cap
api = 'https://api.coinmarketcap.com/v1/ticker/?limit=0'
row_count = 0
resp = requests.get(url=api)
data = json.loads(resp.text)

for x in data:
    # Ticker Data
    id = x["id"]
    # Historical Data
    historical_data_url = 'https://coinmarketcap.com/currencies/' + id + '/historical-data/?start=' + (datetime.datetime.fromtimestamp(
        int(time.time())) - timedelta(days=1)).strftime('%Y%m%d') + '&end=' + (datetime.datetime.fromtimestamp(
        int(time.time())) - timedelta(days=1)).strftime('%Y%m%d')
    page = requests.get(historical_data_url)
    tree = html.fromstring(page.content)
    historical_data = tree.xpath('//td/text()')
    try:
        historical_data_table = np.reshape(np.array(historical_data), (-1, 7))
        for data_historical in historical_data_table:
            date = datetime.datetime.strptime(data_historical[0], "%b %d, %Y").date()
            row_history = [id, date.strftime('%Y-%m-%d'),
                           float(data_historical[1].replace('-', '').replace(',', '') or 0.0),
                           float(data_historical[2].replace('-', '').replace(',', '') or 0.0),
                           float(data_historical[3].replace('-', '').replace(',', '') or 0.0),
                           float(data_historical[4].replace('-', '').replace(',', '') or 0.0),
                           int(data_historical[5].replace('-', '').replace(',', '') or 0),
                           int(data_historical[6].replace('-', '').replace(',', '') or 0)]
            file_historical.write(','.join(str(e) for e in row_history) + '\n')
    except:
        print("Unexpected error", id)

file_historical.close()
# github push
repo_dir = ''
repo = Repo(repo_dir)
file_list = [
    'historical_price.csv'
]
commit_message = 'Update Historical Data'
repo.index.add(file_list)
repo.index.commit(commit_message)
origin = repo.remote('origin')
origin.push()
