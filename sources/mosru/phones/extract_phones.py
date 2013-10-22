#!/usr/bin/env python
# coding: utf-8

import urllib2
from BeautifulSoup import BeautifulSoup

PHONES_URL = "http://www.mos.ru/authority/information/phones/"

def extract():
	p = urllib2.urlopen(PHONES_URL)
	data = p.read()
	p.close()
	soup = BeautifulSoup(data)
	table = soup.find('table', attrs={'class' : 'table'})
	rows = table.find('tbody').findAll('tr', recursive=False)
	topicname = ""
	etop = None
	print 'topicname\tname\tvalue'
	for r in rows:
#		print r
		ths = r.findAll('th')
		if len(ths) > 0:
			pass
			topicname = ths[0].text
			etop = None
#			print topicname
#			print dir(ths[0])
		else:
			tds = r.findAll('td')
			name = tds[0].text
			value = tds[1].text.strip()
			if len(value) == 0:
				etop = name
			else:
				etop = None
			if etop is not None:
				name = name = u" " + etop
			s = [topicname, name, value]
			print ('\t'.join(s)).encode('utf8')
if __name__ == '__main__':
	extract()
