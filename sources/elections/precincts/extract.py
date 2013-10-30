#!/usr/bin/env python
# coding: utf8
# Python script to extract and store data from moscow election comission about Moscow houses

from BeautifulSoup import BeautifulSoup, BeautifulStoneSoup
import  os, urllib2
import json

BASE_URL = 'http://mosgorizbirkom.ru'
BASE_FILE = 'data/refined/moscow_precincts.json'
STREETS_FILE = 'data/raw/streets.json'
STREET_URLPAT = 'http://mosgorizbirkom.ru/precinct/address/%s/search'
STREET_HTML_FILEPAT = 'data/raw/streets_html/street_%s.html'
STREET_FILEPAT = 'data/raw/streets_json/street_%s.json'
BUILDINGS_FILE = 'data/raw/buildings.json'
BUILDING_LIST_URLPAT = "http://mosgorizbirkom.ru/precinct/address/%s/children/byname/?name="
BUILDING_URLPAT = 'http://mosgorizbirkom.ru/precinct/precinct/boundary/byaddress/%s'
BUILDING_HTML_FILEPAT = 'data/raw/buildings_html/build_%s.html'
BUILDING_JSON_FILEPAT = 'data/raw/buildings_json/build_%s.json'
#BUILDING_KEYS = ['house_id', 'url', 'address','year', 'area', 'num_people', 'status']

def table2dict(tab, skip=0, keys=[], keyshift=2):
    rows = []
    i = 0
    for k in tab.findAll('tr', recursive=False):
        i += 1
        if i - skip <= 0: continue
        row = {}
        row['house_id'] = k['class']
        row['url'] = BUILDING_URLPAT % row['house_id']
        tds = k.findAll('td')
        tdslen = len(tds)
        for n in range(0, len(keys), 1):
            try:
                row[keys[n+keyshift]] = tds[n].text
            except:
                pass
        print row
        rows.append(row)
    return rows

def extract_streets():
    """Extracts list of streets. Saves as JSON file"""
    filename = STREETS_FILE
    street_keys = []
    streets = []
    if os.path.exists(filename): return None
    data = open(BASE_FILE, 'r').read()
    all = json.loads(data)
    for o in all['rows']:
        if int(o['street_id']) not in street_keys:
            streets.append({'street_id' : o['street_id'], 'street_name' : o['street_name']})
            street_keys.append(int(o['street_id']))
        else:
            continue

    f = open(filename, 'w')
    f.write(json.dumps(streets, indent=4))
    f.close()

def extract_building_lists():
    """Extracts list of buildings by street. Saves as JSON file for each street"""
    data = open(STREETS_FILE, 'r').read()
    all = json.loads(data)
    for o in all:
        print 'Processing', o['street_id']
        resfilename = STREET_FILEPAT % o['street_id']
        if os.path.exists(resfilename):
            print resfilename, 'exists, skipped'
            continue
        url = BUILDING_LIST_URLPAT % o['street_id']
        try:
            u = urllib2.urlopen(url)
            data = u.read()
            u.close()
        except:
            data = ""
        htmlfilename = STREET_HTML_FILEPAT % o['street_id']
        f = open(htmlfilename, 'w')
        f.write(data)
        f.close()
        resdata = []
        soup = BeautifulSoup(data)
        links = soup.findAll('a')
        for a in links:
            resdata.append({'url' : BASE_URL+a['href'], 'name': a.text})
        f = open(resfilename, 'w')
        f.write(json.dumps(resdata, indent=4))
        f.close()
        print resfilename, 'generated'

def refine_buildings_list():
    """Extracts list of buildings by street. Saves as JSON file for each street"""
    data = open(STREETS_FILE, 'r').read()
    all = json.loads(data)
    buildings = []
    for o in all:
        print 'Processing', o['street_id']
        resfilename = STREET_FILEPAT % o['street_id']
        f = open(resfilename, 'r')
        streetb = json.load(f)
        f.close()
        for b in streetb:
            item = {'building_name': b['name'], 'building_id' : b['url'].rsplit('/', 3)[-3]}
            item.update(o)
            buildings.append(item)
        print 'Street', o['street_id'], 'processed'
    f = open(BUILDINGS_FILE, 'w')
    f.write(json.dumps(buildings, indent=4))
    f.close()


def extract_building_data():
    """Extracts data for each building. Saves as HTML files for future processing"""
    data = open(BUILDINGS_FILE, 'r').read()
    all = json.loads(data)
    for o in all:
        print 'Saving building', o['building_id']
        htmlfilename = BUILDING_HTML_FILEPAT % o['building_id']
        if os.path.exists(htmlfilename):
            print htmlfilename, 'exists, skipped'
            continue
        url = BUILDING_URLPAT % o['building_id']
        try:
            u = urllib2.urlopen(url)
            data = u.read()
            u.close()
        except:
            data = ""
        htmlfilename = BUILDING_HTML_FILEPAT % o['building_id']
        f = open(htmlfilename, 'w')
        f.write(data)
        f.close()
        print htmlfilename, 'saved'

def process_building_data():
    """Extracts data for each building. Saves as HTML files for future processing"""
    data = open(BUILDINGS_FILE, 'r').read()
    all = json.loads(data)
    for o in all:
        print 'Saving building', o['building_id']
        htmlfilename = BUILDING_HTML_FILEPAT % o['building_id']
        if os.path.exists(htmlfilename):
            print htmlfilename, 'exists, skipped'
            continue
        url = BUILDING_URLPAT % o['building_id']
        try:
            u = urllib2.urlopen(url)
            data = u.read()
            u.close()
        except:
            data = ""
        htmlfilename = BUILDING_HTML_FILEPAT % o['building_id']
        f = open(htmlfilename, 'w')
        f.write(data)
        f.close()
        print htmlfilename, 'saved'


def _extract_location(key_tag, prefix='uik_'):
    item = {}
    top_sect = key_tag.parent.parent
#    print top_sect.nextSibling
    address = top_sect.nextSibling
    phone = address.nextSibling.nextSibling
    descr = phone.nextSibling.nextSibling
    ptags = address.findAll('p')
    item[prefix + 'address'] = ptags[1].string
    item[prefix + 'mapurl'] = ptags[0].find('a')['href']
    item[prefix + 'phone'] = phone.findAll('p')[1].text
    item[prefix + 'description'] = descr.find('p').string
#    for k, v in item.items():
#           print k, v
    return item

def parse_building_data():
    """Processes data for each building from HTML files"""
    data = open(BUILDINGS_FILE, 'r').read()
    all = json.loads(data)
    alldata = []
    n = 0
    n_top = len(all)
    for o in all:
        n += 1
        datafilename = BUILDING_JSON_FILEPAT % o['building_id']
        if os.path.exists(datafilename):
            print 'Skipping building %d of %d' % (n, n_top), o['building_id']
            continue
        htmlfilename = BUILDING_HTML_FILEPAT % o['building_id']
        print 'Reading building %d of %d' % (n, n_top), o['building_id']
        f = open(htmlfilename, 'r')
        data = f.read()
        f.close()
        soup = BeautifulStoneSoup(data)
        uik_tag = soup.find('section', attrs={'class': 'precinct-number value'}, recursive=True)
        if uik_tag is None:
            item = o
#            print data
            print '- building is empty'
            alldata.append(o)
            continue
        else:
            print '- building has data'
        ptags = uik_tag.findAll('p')
#        uik = uik_tag.find('p', attrs={'value'}).string
        uik = ptags[1].string
        key_tags = soup.findAll('h4')
        item = {'uik_number' : uik}
        for key_tag in key_tags:

            if key_tag.string == u'избирательная комиссия':
                item.update(_extract_location(key_tag, prefix="uik_"))
            elif key_tag.string == u'место голосования':
                item.update(_extract_location(key_tag, prefix="voteplace_"))
            elif key_tag.string == u'УИК':
                continue
            else:
                print "CRITICAL", key_tag.string
        item.update(o)
        datafilename = BUILDING_JSON_FILEPAT % o['building_id']
        f = open(datafilename, 'w')
        json.dump(item, f, indent=4)
        f.close()
#        alldata.append(item)
        del soup

def merge_json(filepath, storefile):
    files = os.listdir(filepath)
    all = []
    for name in files:
        filename = os.path.join(filepath, name)
        f = open(filename, 'r')
        data = json.load(f)
        f.close()
        print 'Read', name
        all.append(data)
    f = open(storefile, 'w')
    json.dump(all, f, indent=4)
    f.close()




def runall():
    """Run all procedures"""
#    extract_streets()
#    extract_building_lists()
#    refine_buildings_list()
#    extract_building_data()
#    parse_building_data()
    merge_json('data/raw/buildings_json', 'data/raw/allbuildings.json')


if __name__ == "__main__":
    runall()
