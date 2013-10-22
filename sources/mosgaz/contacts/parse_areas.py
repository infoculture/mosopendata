#!/usr/bin/env python

import urllib2
from BeautifulSoup import BeautifulSoup
import json

PAGE_PATH = 'data/pages'


f = open('data/mosgaz_areas.json', 'r')
data = f.read()
f.close()
jdata = json.loads(data)


for r in jdata['rows']:
	id = r['areaid']
	soup = BeautifulSoup(PAGE_PATH + '/%s.html' % id, fromEncoding="windows-1251")
	print soup
	print soup.findAll()
	all = soup.findAll('table', attrs={'class': 'vacTable'})
	for o in all:
		print o
 