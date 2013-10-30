import os, sys
import time
from bs4 import BeautifulSoup as bs
import urllib3
pool = urllib3.PoolManager(10)
head_url = r'http://mosgorizbirkom.ru/precinct/address/'
end1 = r'/search'
end2 = r'/children/byname/?name='

def getstreetdata(num):
	url1 = head_url + str(num) + end1
	url2 = head_url + str(num) + end2
	return (bs(pool.request('GET', url1, retries=20).data.decode('utf-8')).findAll(readonly="readonly"), bs(pool.request('GET', url2, retries=20).data.decode('utf-8')).findAll('a'))

outfile = open(r'address_data.txt', mode = 'w', encoding = 'utf-8')
for num in range(1, 5000):
    try:
        (streetdata, numdata) = getstreetdata(num)
        street = '; '.join(t['value'] for t in streetdata)
        for nn in numdata:
            house = nn.text
            lnk = r'http://mosgorizbirkom.ru/precinct/precinct/boundary/byaddress/' + nn['href'].split(r'/')[-3]
            pg = bs(pool.request('GET', lnk, retries=20).data.decode('utf-8'))
            try:
                uik = pg.find('section', "precinct-number value").find('p', "value").text
                print(uik, street, house, head_url + str(num) + end1, sep ='\t', end = '\n', file = outfile)
            except:
                pass
        print(street)
    except:
        print('failed: ', num)
        
outfile.close()
os.system("shutdown.exe /h")