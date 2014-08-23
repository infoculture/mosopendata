#!/usr/bin/env python
# coding: utf8
# Python script to extract and store data from reformazhkh about Moscow houses

from BeautifulSoup import BeautifulSoup
import  os, urllib2
import json
import re

BASE_URL = 'http://www.reformagkh.ru'
AREAS_URL = 'http://www.reformagkh.ru/myhouse?tid=2280999&sort=alphabet&item=mkd&ajax'
AREAS_FILE = 'data/raw/regions.json'
MUN_URLPAT = 'http://www.reformagkh.ru/myhouse?tid=2280999&sort=alphabet&item=mkd&ajax&tid=%s'
MUN_FILEPAT = 'data/raw/tid_%s.json'
BUILDING_LIST_PAT = 'http://www.reformagkh.ru/myhouse/list?tid=%s&sort=alphabet&item=tp&mkdsort=name&mkdorder=asc&perpage=10000'
BUILDING_URLPAT = 'http://www.reformagkh.ru/myhouse/view/%s/?group=0'
BUILDING_KEYS = ['house_id', 'url', 'address','year', 'area', 'num_people', 'status']

def table2dict(tab, skip=0, keys=[], keyshift=2):
    rows = []
    i = 0
    for k in tab.findAll('tr', recursive=False):
        i += 1
        if i - skip <= 0: continue
        row = {}
        #print k
        tds = k.findAll('td')
        url=tds[0].find('a')['href']
        row['url']=BASE_URL+url
        row['house_id']=re.search('/\d+/',url).group(0).replace('/','')
        tdslen = len(tds)
        for n in range(0, len(keys), 1):
            try:
                row[keys[n+keyshift]] = tds[n].text
            except:
                pass
        #print row
        rows.append(row)
    return rows

def extract_areas():
    """Extracts indicators data by area code. Saves as JSON file"""
    filename = AREAS_FILE
    if os.path.exists(filename): return None
    print "Processing Areas", AREAS_URL
    try:
        u = urllib2.urlopen(AREAS_URL)
    except urllib2.HTTPError:
        return None
    data = u.read()
    u.close()
    soup = BeautifulSoup(data)

    content = soup.find('div', attrs={'class' : 'tables'}, recursive=True).findAll('a')
    areas=[]
    for a in content:
        tid=a['href'].split('=')[1]
        name=str(a.contents[0])
        areas.append({'name':name,'tid':tid})
        print tid,name        
    f = open(filename, 'w')
    f.write(json.dumps(areas, indent=4))
    f.close()
    print "Processing Areas", 'written'

def extract_municipal():
    """Extracts data about municipal areas"""
    f = open(AREAS_FILE, 'r')
    data = f.read()
    f.close()
    js = json.loads(data)
    for record in js:
        filename = MUN_FILEPAT % record['tid']
        if os.path.exists(filename):
            print "Processing. TID %s" % record['tid'], 'skipped'
            continue
        print MUN_URLPAT % record['tid']
        u = urllib2.urlopen(MUN_URLPAT % record['tid'])
        data = u.read()
        u.close()
        soup = BeautifulSoup(data)
        div_muni=soup.find('div', attrs={'class' : 'tables'}, recursive=True)
        div_buildings=soup.find('div', attrs={'id' : 'printAnketa'}, recursive=True)
        mun_areas=[]
        if div_muni:
            content = div_muni.findAll('a')
            for a in content:
                tid=a['href'].split('=')[1]
                name=str(a.contents[0])
                mun_areas.append({'name':name,'tid':tid})
                print tid,name        
        else:
            if div_buildings:
                mun_areas.append({'name':record['name'],'tid':record['tid']})
                print record['tid'],record['name']
            else:
                print "Something wrong :-("
                break
        f = open(MUN_FILEPAT % record['tid'], 'w')
        f.write(json.dumps(mun_areas, indent=4))
        f.close()
        print "Processing. TID %s" % record['tid'], 'written'


def get_buildings_list(url, getlast=True):
    u = urllib2.urlopen(url)
    data = u.read()
    u.close()
    soup = BeautifulSoup(data)
    content = soup.find('div', attrs={'id' : 'printAnketa'}, recursive=True)
#    print url, content
#    print soup
    if getlast:
        itemlist = content.find('div', attrs={'class' : 'item-list'})
        pager = itemlist.find('ul', attrs={'class' : 'pager'})
        plast = pager.find('li', attrs={'class' : 'pager-last'})
        if plast is not None:
            lastpagenum = plast.find('a').string
        else:
            pitems = pager.findAll('li', attrs={'class' : 'pager-item'})
            lastpagenum = pitems[-1].text
    else:
        lastpagenum = None

    tab = content.find('table')
    if tab is not None:
        rows = table2dict(tab, skip=1, keys=BUILDING_KEYS)
    else:
        rows = []
    return rows, lastpagenum


def save_buildings(tid):
    """Saves buildings data by TID"""
    filename = 'data/raw/buildings_%s.json' % tid
    if os.path.exists(filename):
        print "Skipping buildings for mun %s" % tid
        return
    print "Processing buildings for mun %s" % tid
    url = BUILDING_LIST_PAT % tid
    rows, lastp =  get_buildings_list(url, getlast=False)
    print '- processed', url
    f = open(filename, 'w')
    json.dump(rows, f, indent=4)
    f.close()


def extract_buildings_list():
    """Extracts list of buildings for each area"""
    f = open(AREAS_FILE, 'r')
    data = f.read()
    f.close()
    areas = json.loads(data)
    for area in areas:
        f = open(MUN_FILEPAT % area['tid'], 'r')
        data = f.read()
        f.close()
        try:
            muns = json.loads(data)
        except:
            continue
        for mun in muns:
            save_buildings(mun['tid'])
        save_buildings(area['tid'])


def get_buildings_data(tid):
    """Collect buildings data for specific area by TID (territory id)"""
    filename = 'data/raw/buildings_%s.json' % tid
    f = open(filename, 'r')
    rows = json.load(f)
    f.close()
    return rows

def refine_buildings():
    """Prepare data for publishing"""
    idkeys = []
    allrows = []
    allterr = []
    f = open(AREAS_FILE, 'r')
    data = f.read()
    f.close()
    areas = json.loads(data)
    for area in areas:
        f = open(MUN_FILEPAT % area['tid'], 'r')
        data = f.read()
        f.close()
        try:
            muns = json.loads(data)
        except:
            continue
        for mun in muns:
            allterr.append({'name' : mun['name'], 'id' : mun['tid']})
            rows = get_buildings_data(mun['tid'])
            for row in rows:
                if row['house_id'] not in idkeys: idkeys.append(row['house_id'])
                else: continue
                item = {}
                item['area_name'] = mun['name']
                item['area_id'] = mun['tid']
                item['address'] = row['address']
                item['house_year'] = row['year']
                item['house_id'] = row['house_id']
                item['house_area'] = row['area']
                item['num_people'] = row['num_people']
                allrows.append(item)
        rows = get_buildings_data(area['tid'])
        if len(rows) > 0:
            allterr.append({'name' : area['name'], 'id' : area['tid']})
        for row in rows:
            if row['house_id'] not in idkeys: idkeys.append(row['house_id'])
            else: continue
            item = {}
            item['area_name'] = mun['name']
            item['area_id'] = mun['tid']
            item['address'] = row['address']
            item['house_year'] = row['year']
            item['house_id'] = row['house_id']
            item['house_area'] = row['area']
            item['num_people'] = row['num_people']
            allrows.append(item)
    f = open('data/refine/buildings.json', 'w')
    json.dump(allrows, f, indent=4)
    f.close()
    f = open('data/refine/areas.json', 'w')
    json.dump(allterr, f, indent=4)
    f.close()


def runall():
    """Run all procedures"""
    extract_areas()
    extract_municipal()
    extract_buildings_list()
    refine_buildings()

if __name__ == "__main__":
    runall()