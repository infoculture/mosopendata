#!/usr/bin/env python
# coding: utf8
# Python script to extract and store data from data.mos.ru

from BeautifulSoup import BeautifulSoup
import  os, urllib2
import json

QUAL_URLPAT = 'http://www.mosvodokanal.ru/wq/php/wq.php/qualBlocks/QualZone?cter=%s'
BASE_URL = 'http://www.mosvodokanal.ru'
REGIONS_FILE = 'data/regions.json'

INDICATORS = {
    '1000': u'Неизвестно (1000)',
    '1001': u'Неизвестно (1001)',
    '1002': u'Запах при 20C',
    '1003': u'Неизвестно (1003)',
    '1004': u'Цветность',
    '1005': u'Мутность',
    '1006': u'Водородный показатель (pH)',
    '1013': u'Железо общее',
    '1050': u'Термотолерантные колиформные бактерии (ТКБ)',
    '1053': u'Общее микробное число (ОМЧ)',
    '1121': u'Остаточный хлор',
    '1200': u'Запах при 60C',
    '5147': u'Неизвестно (5147)',
    '5148': u'Неизвестно (5148)',
    '5501': u'Общие колиформные бактерии (ОКБ)',

}


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


def dump_all_as_csv():
    """Loads raw JSON files and writes single CSV """
    f = open(REGIONS_FILE, 'r')
    regs = json.loads(f.read())
    f.close()
    keys = ['dtfrom', 'dtto', 'zones', 'ind_id', 'ind_name', 'code', 'regname',  'value']
    resfilename = 'data/all.csv'
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
        dtfrom = js['data']['dtfrom']
        dtto = js['data']['dtto']
        zones = []
        for k in js['data']['zones']:
            zones.append(k['id'])

        for v in js['data']['params']:
            s = '\t'.join([dtfrom, dtto, '|'.join(zones), v['id'], INDICATORS[v['id']], code,  regname, unicode(v['value'])]).encode('utf8') + '\n'
            f.write(s)
    f.close()



if __name__ == "__main__":
    #process()
    for k in ['1121', '1004', '1005', '1002', '1006', '1013', '1050', '1053', '1200', '5501']:
        dump_csv_by_key(k)
    dump_all_as_csv()