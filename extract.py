#!/usr/bin/env python
# coding: utf8

from BeautifulSoup import BeautifulSoup
import sys, os, urllib2
import json

REGISTRY_URL = 'http://data.mos.ru/datasets/param/'
BASE_URL = 'http://data.mos.ru'
JSON_URL = 'http://data.mos.ru/datasets/aaData?id=%s'

def extract_dataset(url):
    id = url.rsplit('/', 2)[-2]
    if os.path.exists('data/%s.csv' % id ): return None
    u = urllib2.urlopen(BASE_URL + url)
    data = u.read()
    u.close()
    soup = BeautifulSoup(data)
    keys = []
    tab = soup.find('tfoot', attrs={'class': 'dataTable_filters'})
    headers = tab.findAll('th')
    for h in headers:
        keys.append(h['name'])
    u = urllib2.urlopen(JSON_URL % id)
    data = u.read()
    u.close()
    try:
        js = json.loads(data)
    except ValueError:
        return None
    f = open('data/%s.csv' %(id), 'w')
    s = u'\t'.join(keys).encode('utf8')
    f.write(s + '\n')
    rows = js['aaData']
    for row in rows:
        s = u'\t'.join(row).encode('utf8')
        f.write(s + '\n')
    return keys
    
    
def process():
    u = urllib2.urlopen(REGISTRY_URL)
    data = u.read()
    u.close()
    soup = BeautifulSoup(data)
    tab = soup.find('table', attrs={'class' : 'tablereestr'})
    rows = tab.findAll('tr')
    keys = ['name', 'url', 'description', 'source', 'theme', 'pubdate', 'format']    
    print '\t'.join(keys).encode('utf8')
    rows = tab.findAll('tr')    
    for row in rows:
        item = []
        tds = row.findAll('td')
        if len(tds) == 0: continue
        if len(tds) != 3: continue
        href = tds[0].find('a')
        item.append(href.string)
        item.append(href['href'])
        item.append(tds[0].find('p', attrs={'class' : 'description'}).string)
        item.append(tds[0].find('p', attrs={'class' : 'source'}).string)
        item.append(tds[0].find('input')['name'])
        item.append(tds[1].string)
        item.append(tds[2].string)
        s = u'\t'.join(item)
        print s.encode('utf8')
        extract_dataset(item[1])
    pass
    
    

if __name__ == "__main__":
    process()