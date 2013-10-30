#!/usr/bin/env python
# coding: utf-8

import urllib2
from BeautifulSoup import BeautifulSoup
import json
NOTICE_URL = "http://notice.crc.ru/?action=search&&code_region=77&&n4=000&page=%d"

PAGES = range(1, 273, 1)


def process_all():
    allrec = []
    for p in PAGES:
        allrec.extend(extract(p))
    json.dump(allrec, open('data/allorgs.json', 'w'), indent=4)

def table2dict(tab):
    keys = []
    rows = []
    for k in tab.find('thead').find('tr').find('td'):
        keys.append(k)
    for k in tab.findAll('tr', recursive=False):
        row = {}
        tds = k.findAll('td')
        tdslen = len(tds)
        for n in range(0, len(keys), 1):
            try:
                row[keys[n]] = tds[n].text
            except:
                pass
        rows.append(row)
    return rows

def extract(pageid):
    p = urllib2.urlopen(NOTICE_URL % pageid)
    data = p.read()
    p.close()
    records = []
    soup = BeautifulSoup(data)
    table = soup.find('table', attrs={'class' : 'tlist'})
    rows = table.findAll('tr', recursive=False)
    record = {}
    for r in rows:
        tds = r.findAll('td')
        if len(tds) == 1:
            if len(record.keys()) > 0:
                records.append(record)
            record = {}
        elif len(tds) == 0:
            continue
        else:
            tab2 = tds[1].find('table', recursive=False)
            if tab2:
                value = table2dict(tab2)
            else:
                value = tds[1].text.strip().replace('&nbsp;', ' ').strip()
            key = tds[0].text.replace('&nbsp;', ' ').strip()
            print key
            record[key] = value
    records.append(record)
    return records
if __name__ == '__main__':
    process_all()
