#!/usr/bin/env python
# coding: utf-8

import urllib2
from BeautifulSoup import BeautifulSoup

HOTLINE_URL = "http://www.mos.ru/authority/hotlines/%s/"

PAGES = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '13', '14', '15', '20', '30']

SCHEMAS = {
	'01': ['phone', 'name', 'org'],
	'02': ['name', 'phone'],
	'03': ['name', 'phone'],
	'04': ['name', 'phone'],
	'05': ['phone', 'name', 'org'],
	'06': ['name', 'phone'],
	'07': ['phone', 'name', 'org'],
	'08': ['phone', 'name', 'org'],
	'09': ['name', 'phone'],
	'10': ['phone', 'name', 'org'],
	'11': ['name', 'phone'],
	'13': ['name', 'phone'],
	'14': ['phone', 'name', 'org'],
	'15': ['name', 'phone'],
	'20': ['phone', 'name', 'org'],
	'30': ['name', 'phone'],
}

def extract(pageid):
	p = urllib2.urlopen(HOTLINE_URL % pageid)
#	print HOTLINE_URL % pageid
	data = p.read()
	p.close()
	soup = BeautifulSoup(data)
	topicname = soup.find('h1').string
	table = soup.find('table', attrs={'class' : 'table'})
	rows = table.findAll('tr', recursive=False)
	etop = None
	schema = SCHEMAS[pageid]
	for r in rows:
		tds = r.findAll('td')
		if len(tds) == 0: continue
		if 'org' in schema:
			org = tds[schema.index('org')].text
		else:
			org = ""
		name =  tds[schema.index('name')].text.replace('\n', ' ')
		phone =  tds[schema.index('phone')].text.replace('\n', ' ')
		s = [topicname, org, name, phone]
		print ('\t'.join(s)).encode('utf8')
if __name__ == '__main__':
	print 'topicname\torg\tname\tphone'
	for p in PAGES:
		extract(p)
