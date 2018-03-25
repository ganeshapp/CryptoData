import json, requests
import datetime
import time
from git import Repo
import ast

# Get Load Date
sysdate = datetime.datetime.fromtimestamp(int(time.time())).strftime('%Y-%m-%d %H:%M:%S')

# All the Files
file_events = open('/home/gapp/CryptoData/events.csv', 'w')

# All the headers
header_events = ['id','coin_id','coin_name', 'coin_symbol', 'date_event', 'created_date', 'title', 'description', 'category_id', 'category_name', 'proof', 'source', 'is_hot', 'vote_count', 'positive_vote_count', 'percentage', 'can_occur_before', 'load_date']

# Write headers into files
file_events.write(','.join(str(e) for e in header_events) + '\n')

# Get ticker data from coin market cap
# api = 'https://api.coinmarketcap.com/v1/ticker/?limit=0'
row_count = 0
# resp = requests.get(url=api)
# data = json.loads(resp.text)

authApi = 'https://api.coinmarketcal.com/oauth/v2/token?grant_type=client_credentials&client_id=107_5qaox6okwkcgg44o0sgkkwkkcc4ggs8o88swg8ssgok40csgg0&client_secret=1vsi861hyc9w8w0cwckgssokosw0wk08g8kocksg8so4ck44ws'
resp = requests.get(url=authApi)
data = json.loads(resp.text)
access_token = data["access_token"]
i=0
while i<100:
    i = i + 1
    try:
        eventApi = 'https://api.coinmarketcal.com/v1/events?access_token=' + access_token + '&page=' + str(i) + '&max=200&dateRangeStart=01%2F01%2F2010'
        resp = requests.get(url=eventApi)
        data = json.loads(resp.text)
        if (str(data[0]) == 'code'):
            break
        for x in data:
            try:
                id = x["id"]
                title = x["title"]
                date_event = x["date_event"].split('T', 1)[0]
                created_date = datetime.datetime.strptime(x["created_date"].split('T', 1)[0] +' '+ x["created_date"].split('T', 1)[1].split('+', 1)[0], '%Y-%m-%d %H:%M:%S')
                description = str(x["description"] or '').replace('\n', '').replace(',', '').replace('\r', '').replace('"', '').strip()
                proof = x["proof"]
                source = x["source"]
                is_hot = x["is_hot"]
                vote_count = x["vote_count"]
                positive_vote_count = x["positive_vote_count"]
                percentage = x["percentage"]
                can_occur_before = x["can_occur_before"]
                coins = json.loads(json.dumps(ast.literal_eval(str(x["coins"]))))
                for y in coins:
                    coin_id = y["id"]
                    coin_name = y["name"]
                    coin_symbol = y["symbol"]
                    categories = json.loads(json.dumps(ast.literal_eval(str(x["categories"]))))
                    for z in categories:
                        category_id = z["id"]
                        category_name = z["name"]
                        row_event = [id,coin_id,coin_name, coin_symbol, date_event, created_date, title, description, category_id, category_name, proof, source, is_hot, vote_count, positive_vote_count, percentage, can_occur_before, sysdate]
                        file_events.write(','.join(str(e) for e in row_event) + '\n')
            except Exception as e:
                print(x)
                print("for ith loop, failed for id", i, id, coin_id)
                print(e)
    except  Exception as e:
        print("quit loop at ", i)
        print(e)
        break

file_events.close()
# github push
repo_dir = '/home/gapp/CryptoData/'
repo = Repo(repo_dir)
file_list = [
    '/home/gapp/CryptoData/events.csv'
]
commit_message = 'Reset Events Data'
repo.index.add(file_list)
repo.index.commit(commit_message)
origin = repo.remote('origin')
origin.push()
print("completed")