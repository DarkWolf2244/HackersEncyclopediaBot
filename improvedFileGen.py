import requests
import lxml.html as lh
import json
import os
from time import sleep
from pprint import pprint

url = "https://hackersthegame.fandom.com/wiki/AI_Squid"

page = requests.get(url) 
scrape = lh.fromstring(page.content)    

tables = scrape.xpath('//table')

skip = ['AvailabilityStatistics', 
    'ConnectivityStatistics', 
    'NodeStatistics', 'HackersWikia',
    'Maximum Offensive Program Levels', 'Maximum Defensive Program Levels',
    'Maximum Stealth Program Levels', 'A.I.Statistics',
    'BusinessNodeLimits','SecurityNodeLimits','HackingNodeLimits',
    'ArtificialIntelligenceNodeLimits', 'Bold','ColorText',
    'CompilationStatistics','ProgramStatistics']

data = {}

ROWS = 21 #SET THIS TO THE NUMBER OF ROWS
TABLES_COUNT = 3

for i in range(1, ROWS + 1): data[str(i)] = {}

def content(obj):
    return obj.text_content().replace('\n', '').replace(' ', '')

cnt = 0

for tbl_data in tables:
    tbl_content = content(tbl_data)
    if any([i in tbl_content for i in skip]): continue
    
    cnt += 1
    
    if cnt > TABLES_COUNT: break
    title, table = tbl_data
    
    columns = [content(i) for i in table[0]]
    del table[0]
    for row in table:
        val = [content(i) for i in row]
        if val[0] == 'Totals' or val[0] == 'Total': continue
        for i in range(1, len(columns)):
            data[val[0]][columns[i]] = val[i].replace('B', '')


td = scrape.xpath('//b')
img = scrape.xpath('//img')

data2 = []
cnt = 0

for i in td:
    f = i.text_content().replace('\n', '')
    if any(i in f for i in skip): continue
    if "Level" in f and len(f.split()) > 1:
        data2.append([f, []])
pprint(data2)
print(len(data2))

for i in img:
    print(i.attrib['alt'],end = '     ')
    print("Evolver" in i.attrib['alt'])
    if ".png" in i.attrib['alt'] and "Squid" in i.attrib['alt']:
        data2[cnt][1] = i.attrib['data-src'] 
        cnt += 1
        if cnt >= len(data2):
            break

cur_data = [i for i in data2]
data2 = []

for i, j in cur_data:
    if '-' in i:
        i = i.split()[1].split('-')
        for k in range(int(i[0]), int(i[1]) + 1): data2.append([str(k), j])
    else:
        data2.append([i.split(' ')[1], j])

for i in data2:
    data[str(i[0])]['imageAddress'] = i[1]
    
print(json.dumps(data, indent = 4))

with open("aisquid.json", "w") as f:
    json.dump(data, f, indent = 4)
