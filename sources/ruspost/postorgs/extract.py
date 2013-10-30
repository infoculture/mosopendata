#!/usr/bin/env python

import urllib2
from BeautifulSoup import BeautifulSoup
import json
URL = 'http://www.xn--80aaaf5bvagpog6c7f.xn--p1ai/issue/id15617/'

def process():
    print "Extracting data"
    u = urllib2.urlopen(URL)
    data = u.read()
    u.close()
    soup = BeautifulSoup(data)
    jsond = soup.find('div', attrs={'id' : 'ymaps-map-geo_objects'}).text
    print jsond
    js = json.loads(jsond)

    print "Saving data"
    f = open('data/postorgs.json', 'w')
    f.write(json.dumps(js, indent=4))
    f.close()

    
if __name__ == "__main__":
    process()