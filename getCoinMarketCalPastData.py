from lxml import html
import requests
import numpy as np
import json, requests
import datetime
import time
from git import Repo

# Get Load Date
sysdate = datetime.datetime.fromtimestamp(int(time.time())).strftime('%Y-%m-%d %H:%M:%S')

file_cal = open('coin_calendar_past.csv', 'w')

header_cal = ['event_date', 'name', 'symbol', 'added_on', 'event_name', 'description', 'report_date']

file_cal.write(','.join(str(e) for e in header_cal) + '\n')

# Coin Market Cal Past Event Data
cal_data_url = 'https://coinmarketcal.com/pastevents?form%5Bfilter_by%5D=hot_events&form%5Bsubmit%5D=&page=1'
cal_page = requests.get(cal_data_url)
cal_tree = html.fromstring(cal_page.content)
# cal_data = cal_tree.xpath('//div[@class="content-box-general"]/h5/strong/text()|//div[@class="content-box-general"]/div[@class="content-box-info"]/p/text()|//div[@class="content-box-general"]/div[@class="content-box-info"]/a/attribute::href')
cal_data = cal_tree.xpath(
    '//div[@class="content-box-general"]/h5/strong/text()|//div[@class="content-box-general"]/h5/text()|//div[@class="content-box-general"]/h5/strong/span/attribute::data-content|//div[@class="content-box-general"]/div[@class="content-box-info"]/p/text()')
#print(cal_data)
j=0
cleaned_list=[]
while j<len(cal_data):
    element = cal_data[j].replace('\n','').replace(',','').replace('\r','').replace('"', '').strip()
    if not (element == '' or element.startswith('(or')):
        if (element == 'Merry Christmas'):
            cleaned_list.append('useless (useless)')
        cleaned_list.append(element)
    j += 1
print('length:',len(cleaned_list))
cal_data_table = np.reshape(np.array(cleaned_list), (-1, 6))
for data_cal in cal_data_table:
    event_date = datetime.datetime.strptime(data_cal[0], "%d %B %Y").date()
    added_date = datetime.datetime.strptime(
        data_cal[3].replace('(Added ', '').replace(')', ''), "%d %B %Y").date()
    row_cal = [event_date,
               data_cal[1].split('(', 1)[0].strip(),
               data_cal[1].split('(', 1)[1].split(')')[0],
               added_date,
               data_cal[2],
               data_cal[4],
               # 'https://coinmarketcal.com'+data_cal[4].replace("\n", '').strip(),
               # data_cal[5].replace("\n", '').strip(),
               sysdate]
    file_cal.write(','.join(str(e) for e in row_cal) + '\n')
    print(','.join(str(e) for e in row_cal) + '\n')

# Pagenation loop
page_data = cal_tree.xpath('//i[@class="fa fa-angle-double-right"]/../attribute::href')
print(page_data[0].split('=', -1)[3])
page_base_url = "https://coinmarketcal.com/?form%5Bfilter_by%5D=hot_events&form%5Bsubmit%5D=&page="
i = 2

while i < int(page_data[0].split('=', -1)[3], 0):
    cal_data_url = 'https://coinmarketcal.com/pastevents?form%5Bfilter_by%5D=hot_events&form%5Bsubmit%5D=&page=' + str(i)
    print(i,cal_data_url)
    cal_page = requests.get(cal_data_url)
    cal_tree = html.fromstring(cal_page.content)
    cal_data = cal_tree.xpath(
        '//div[@class="content-box-general"]/h5/strong/text()|//div[@class="content-box-general"]/h5/text()|//div[@class="content-box-general"]/h5/strong/span/attribute::data-content|//div[@class="content-box-general"]/div[@class="content-box-info"]/p/text()')
    # print(cal_data)
    # print(len(cal_data))
    j = 0
    cleaned_list = []
    while j < len(cal_data):
        element = cal_data[j].replace('\n', '').replace(',', '').replace('\r', '').replace('"', '').strip()
        if not (element == '' or element.startswith('(or')):
            if (element == 'Merry Christmas'):
                cleaned_list.append('useless (useless)')
            cleaned_list.append(element)
        j += 1
    cal_data_table = np.reshape(np.array(cleaned_list), (-1, 6))
    for data_cal in cal_data_table:
        event_date = datetime.datetime.strptime(data_cal[0], "%d %B %Y").date()
        added_date = datetime.datetime.strptime(
            data_cal[3].replace('(Added ', '').replace(')', ''), "%d %B %Y").date()
        row_cal = [event_date,
                   data_cal[1].split('(', 1)[0].strip(),
                   data_cal[1].split('(', 1)[1].split(')')[0],
                   added_date,
                   data_cal[2],
                   data_cal[4],
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
    'coin_calendar_past.csv'
]
commit_message = 'Updated Calendar Data File'
repo.index.add(file_list)
repo.index.commit(commit_message)
origin = repo.remote('origin')
origin.push()
print('Github Push Finished')
