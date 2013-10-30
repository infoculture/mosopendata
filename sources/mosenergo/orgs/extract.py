#!/usr/bin/env python
# coding: utf-8

import urllib2
from BeautifulSoup import BeautifulSoup, BeautifulStoneSoup
import json
URL = "http://www.mosenergo.ru/catalog/228.aspx"



def process_all():
    p = urllib2.urlopen(URL)
    data = p.read()
    p.close()
    records = []
    soup = BeautifulStoneSoup(data)
    table = soup.find('table', attrs={'class' : 'MsoNormalTable'})
    print table
    allrec = table2dict(table, keys=['id', 'name', 'address'], skip=2)
    json.dump(allrec, open('data/allorgs.json', 'w'), indent=4)

def table2dict(tab, keys=[]):
    rows = []
    if len(keys) == 0:
        for k in tab.find('thead').find('tr').find('td'):
            keys.append(k)
    for k in tab.find('tbody').findAll('tr'):#, recursive=False):
        row = {}
        print k
        tds = k.findAll('td')
        tdslen = len(tds)
        for n in range(0, len(keys), 1):
            try:
                row[keys[n]] = tds[n].text
                print row[keys[n]]
            except:
                pass
        rows.append(row)
    return rows


if __name__ == '__main__':
    process_all()
