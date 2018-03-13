from lxml import html
import requests
import numpy as np
import json, requests
import datetime
import time
from git import Repo

# Get Load Date
sysdate = datetime.datetime.fromtimestamp(int(time.time())).strftime('%Y-%m-%d %H:%M:%S')

file_cal = open('coin_calendar.csv', 'w')

header_cal = ['event_date', 'name', 'symbol', 'added_on', 'event_name','description', 'report_date']

file_cal.write(','.join(str(e) for e in header_cal) + '\n')

# Coin Gecko Scores for Coins data
cal_data_url = 'https://coinmarketcal.com/?form%5Bfilter_by%5D=hot_events&form%5Bsubmit%5D=&page=1'
cal_page = requests.get(cal_data_url)
cal_tree = html.fromstring(cal_page.content)
# cal_data = cal_tree.xpath('//div[@class="content-box-general"]/h5/strong/text()|//div[@class="content-box-general"]/div[@class="content-box-info"]/p/text()|//div[@class="content-box-general"]/div[@class="content-box-info"]/a/attribute::href')
cal_data = cal_tree.xpath(
    '//div[@class="content-box-general"]/h5/strong/text()|//div[@class="content-box-general"]/h5/text()|//div[@class="content-box-general"]/div[@class="content-box-info"]/p/text()')
# print(cal_data)
cal_data_table = np.reshape(np.array(cal_data), (-1, 11))
for data_cal in cal_data_table:
    event_date = datetime.datetime.strptime(data_cal[0], "%d %B %Y").date()
    added_date = datetime.datetime.strptime(
        data_cal[8].replace("\n", '').replace(',', '').replace('(Added ', '').replace(')', ''), "%d %B %Y").date()
    row_cal = [event_date,
               data_cal[4].replace("\n", '').strip().split('(', 1)[0].strip(),
               data_cal[4].replace("\n", '').split('(', 1)[1].split(')')[0],
               added_date,
               data_cal[6].replace("\n", '').replace("\r", '').strip().replace(",", '').replace('"', ''),
               data_cal[9].replace("\n", '').replace("\r", '').strip().replace(",", '').replace('"', ''),
               # 'https://coinmarketcal.com'+data_cal[4].replace("\n", '').strip(),
               # data_cal[5].replace("\n", '').strip(),
               sysdate]
    file_cal.write(','.join(str(e) for e in row_cal) + '\n')
    # print(','.join(str(e) for e in row_cal) + '\n')

# Pagenation loop
page_data = cal_tree.xpath('//i[@class="fa fa-angle-double-right"]/../attribute::href')
# print(page_data[0].split('=', -1)[3])
page_base_url = "https://coinmarketcal.com/?form%5Bfilter_by%5D=hot_events&form%5Bsubmit%5D=&page="
i = 2

while i < int(page_data[0].split('=', -1)[3], 0):
    cal_data_url = 'https://coinmarketcal.com/?form%5Bfilter_by%5D=hot_events&form%5Bsubmit%5D=&page=' + str(i)
    cal_page = requests.get(cal_data_url)
    cal_tree = html.fromstring(cal_page.content)
    cal_data = cal_tree.xpath(
        '//div[@class="content-box-general"]/h5/strong/text()|//div[@class="content-box-general"]/h5/text()|//div[@class="content-box-general"]/div[@class="content-box-info"]/p/text()')
    # print(cal_data)
    # print(len(cal_data))
    cal_data_table = np.reshape(np.array(cal_data), (-1, 11))
    for data_cal in cal_data_table:
        event_date = datetime.datetime.strptime(data_cal[0], "%d %B %Y").date()
        added_date = datetime.datetime.strptime(
            data_cal[8].replace("\n", '').replace(',', '').replace('(Added ', '').replace(')', ''), "%d %B %Y").date()
        row_cal = [event_date,
                   data_cal[4].replace("\n", '').strip().split('(', 1)[0].strip(),
                   data_cal[4].replace("\n", '').split('(', 1)[1].split(')')[0],
                   added_date,
                   data_cal[6].replace("\n", '').replace("\r", '').strip().replace(",", '').replace('"', ''),
                   data_cal[9].replace("\n", '').replace("\r", '').strip().replace(",", '').replace('"', ''),
                   sysdate]
        file_cal.write(','.join(str(e) for e in row_cal) + '\n')
        # print(','.join(str(e) for e in row_cal) + '\n')
    i += 1

print('Completed')
file_cal.close()
print('Github Push')
# github push
repo_dir = ''
repo = Repo(repo_dir)
file_list = [
    'coin_calendar.csv'
]
commit_message = 'Updated Calendar Data File'
repo.index.add(file_list)
repo.index.commit(commit_message)
origin = repo.remote('origin')
origin.push()
print('Github Push Finished')
