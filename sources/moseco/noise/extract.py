#!/usr/bin/env python
# coding: utf-8

import urllib2
from BeautifulSoup import BeautifulSoup, BeautifulStoneSoup
import json
URL = "http://www.mosecom.ru/noise/territ/noise_stroy_pl_2013.php"



def process_all():
    p = urllib2.urlopen(URL)
    data = p.read()
    p.close()
    records = []
    soup = BeautifulSoup(data)
    table = soup.find('table', attrs={'class' : 'MsoNormalTable'})
    print table
    allrec = table2dict(table, keys=['okrug', 'area','address', 'source', 'numrequests', 'checkdate', 'results', 'changes'], skip=2)
    json.dump(allrec, open('data/records.json', 'w'), indent=4)

def table2dict(tab, keys=[], skip=0):
    rows = []
    if len(keys) == 0:
        for k in tab.find('thead').find('tr').find('td'):
            keys.append(k)
    for k in tab.findAll('tr'):#, recursive=False):
        row = {}
        print k
        tds = k.findAll('td')
        tdslen = len(tds)
        for n in range(0, len(keys), 1):
            try:
                row[keys[n]] = tds[n].text.replace('\n', ' ')
                print row[keys[n]]
            except:
                pass
        rows.append(row)
    return rows


if __name__ == '__main__':
    process_all()
