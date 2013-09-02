#!/usr/bin/env python
# coding: utf8
# Python script to extract and store data from data.mos.ru

from BeautifulSoup import BeautifulSoup
import  os, urllib2
import json

QUAL_URLPAT = 'http://www.mosvodokanal.ru/wq/php/wq.php/qualBlocks/QualZone?cter=%s'
BASE_URL = 'http://www.mosvodokanal.ru'
REGIONS_FILE = 'data/regions.json'

def extract_dataset(code):
    """Extracts indicators data by area code. Saves as JSON file"""
    filename = 'data/raw/%s.json' % code
    if os.path.exists(filename): return None
    try:
        u = urllib2.urlopen(QUAL_URLPAT % code)
    except urllib2.HTTPError:
        return None
    data = u.read()
    js = json.loads(data)
    u.close()
    f = open(filename, 'w')
    f.write(json.dumps(js, indent=4))
    f.close()



def process():
    """Processes all areas for indicators values. Saves as individual JSON files"""
    f = open(REGIONS_FILE, 'r')
    regs = json.loads(f.read())
    f.close()
    for r in regs:
        code = r['code']
        print 'Processing', code
        extract_dataset(code)
    pass


def dump_csv_by_key(key="1121"):
    """Loads raw JSON files and writes single CSV with selected indicator value"""
    ID_KEY = key
    f = open(REGIONS_FILE, 'r')
    regs = json.loads(f.read())
    f.close()
    keys = ['key', 'code', 'regname',  'value']
    resfilename = 'data/indicators/%s.csv' % (key)
    f = open(resfilename, 'w')
    s = '\t'.join(keys).encode('utf8') + '\n'
    f.write(s)
    for r in regs:
        code = r['code']
        code = str(code)
        regname = r['name']
        filename = 'data/raw/%s.json' % code
        data = open(filename, 'r').read()
        try:
            js = json.loads(data)
        except:
            print 'Error', data
            continue
        for v in js['data']['params']:
            if v['id'] == ID_KEY:
                s = '\t'.join([v['id'], code,  regname, unicode(v['value'])]).encode('utf8') + '\n'
                f.write(s)
    f.close()



if __name__ == "__main__":
    #process()
    for k in ['1121', '1004', '1005', '1002', '1006', '1013', '1050', '1053', '1200', '5501']:
        dump_csv_by_key(k)