#!/usr/bin/env python

import urllib2
from BeautifulSoup import BeautifulSoup

URL = 'http://www.mos-gaz.ru/bitrix/othermodules/intellidb/getrows.php'

print "Extracting data"
u = urllib2.urlopen(URL)
data = u.read()
u.close()
print "Saving data"
f = open('data/streets.html', 'w')
f.write(data)
f.close()

print "Processing data"
soup = BeautifulSoup(data)
for o in soup.findAll('span'):
    inp = o.find('input')
    v = inp['value']
    a = o.find('a')
    name = a.string
    addrinfo = o.contents[-1]    
    s = u'\t'.join([name, v, addrinfo])
    print s.encode('utf8')
    
    
 