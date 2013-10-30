#!/usr/bin/env python
# coding: utf-8

import urllib2
from BeautifulSoup import BeautifulSoup
import json
NOTICE_URL = "http://notice.crc.ru/?action=search&&code_region=77&&n4=000&page=%d"

def process_all_okun():
    data =json.load(open('data/moscow_rospotreb_notices.json', 'r'))
    okun = []
    print 'okun_code'
    for row in data['rows']:
        val = row['okun_codes']
        if val is not None and len(val) > 0:
            codes = val.split(',')
            for code in codes:
                if code not in okun:
                    okun.append(code)
    okun.sort()
    for k in okun:
        print k.encode('utf8')

def process_all_okved():
    data =json.load(open('data/moscow_rospotreb_notices.json', 'r'))
    okun = []
    print 'okved_code'
    for row in data['rows']:
        val = row['okved_codes']
        if val is not None and len(val) > 0:
            codes = val.split(',')
            for code in codes:
                if code not in okun:
                    okun.append(code)
    okun.sort()
    for k in okun:
        print k.encode('utf8')

if __name__ == '__main__':
#    process_all_okun()
    process_all_okved()
