#!/usr/bin/env python
# coding: utf8
# Python script to extract and store data from data.mos.ru

from BeautifulSoup import BeautifulSoup
import  os, urllib2
import json

REGISTRY_URL = 'http://data.mos.ru/datasets'
BASE_URL = 'http://data.mos.ru'

def extract_dataset(url, id):
    filename = 'thedata/%s.csv' % id
    if os.path.exists(filename): return None
    try:
        u = urllib2.urlopen(url)
    except urllib2.HTTPError:
        return None
    data = u.read()
    u.close()
    f = open('thedata/%s.csv' % id, 'w')
    f.write(data)
    f.close()

def open_url(url):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.60 Safari/537.17')]
    response = opener.open(url)
    return response


def process():
    u = open_url(REGISTRY_URL)
    data = u.read()
    u.close()
    soup = BeautifulSoup(data)
    tab = soup.find('table', attrs={'id' : 'data_table'})
    keys = ['name', 'url', 'id',  'source', 'theme']
    print
    tbody = tab.find('tbody')
    rows = tbody.findAll('tr')
    s = '\t'.join(keys).encode('utf8') + '\n'
    print s.strip()
    f = open('datasets.csv', 'w')
    f.write(s)
    for row in rows:
        item = []
        tds = row.findAll('td')
        if len(tds) == 0: continue
        if len(tds) < 4: continue
        celldiv = tds[1].find('div')
        id = row['id_dataset']
        href = 'http://data.mos.ru/datasets/%s' %(id)
        down_href = 'http://data.mos.ru/datasets/download/%s' %(id)
        item.append(celldiv.next.strip())
        item.append(href)
        item.append(id)
        item.append(tds[3].string.strip())
        item.append(tds[2].string.strip())
#        print item
        s = (u'\t'.join(item) + '\n').encode('utf8')
        print s.strip()
        f.write(s)

        extract_dataset(down_href, id)
    pass
    
    

if __name__ == "__main__":
    process()