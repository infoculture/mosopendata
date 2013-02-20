#!/usr/bin/env python
# coding: utf8
# Python script to extract and store data from data.mos.ru

from BeautifulSoup import BeautifulSoup
import sys, os, urllib2
import json

REGISTRY_URL = 'http://data.mos.ru/datasets/param/'
BASE_URL = 'http://data.mos.ru'
JSON_URL = 'http://data.mos.ru/datasets/aaData?id=%s'

def extract_dataset(url, datasetid):
    id = url.rsplit('/', 2)[-2]
    if os.path.exists('thedata/%s.csv' % id ): return None
    print BASE_URL + url
    try:
        u = urllib2.urlopen(BASE_URL + url)
    except urllib2.HTTPError:
        return None
    data = u.read()
    u.close()
    soup = BeautifulSoup(data)
    keys = []
    tab = soup.find('tfoot', attrs={'class': 'dataTable_filters'})
    headers = tab.findAll('th')
    for h in headers:
        keys.append(h['name'])
    print JSON_URL % datasetid
    u = urllib2.urlopen(JSON_URL % datasetid)
    data = u.read()
    u.close()
    try:
        js = json.loads(data)
    except ValueError:
        return None
    f = open('thedata/%s.csv' %(id), 'w')
    s = u'\t'.join(keys).encode('utf8')
    f.write(s + '\n')
    rows = js['aaData']
    for row in rows:
        s = u'\t'.join(row).encode('utf8')
        f.write(s + '\n')
    return keys

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
    tab = soup.find('table', attrs={'class' : 'tablereestr'})
    rows = tab.findAll('tr')
    keys = ['name', 'url', 'id', 'description', 'source', 'theme', 'pubdate', 'format']
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
        item.append(href['href'].split('_', 1)[0].rsplit('/', 1)[-1])
        item.append(tds[0].find('p', attrs={'class' : 'description'}).string)
        item.append(tds[0].find('p', attrs={'class' : 'source'}).string)
        item.append(tds[0].find('input')['name'])
        item.append(tds[1].next.next.next)
        item.append(tds[2].string)
        s = u'\t'.join(item)
        print s.encode('utf8')
        extract_dataset(item[1], item[2])
    pass
    
    

if __name__ == "__main__":
    process()