#!/usr/bin/env python
# coding: utf8

import os, sys
from BeautifulSoup import BeautifulSoup

def xml2csv(filename):
    """Transforms budget.mos.ru XML to CSV files"""
    f = open(filename, 'r')
    soup = BeautifulSoup(f)
    dirname = filename.rsplit('.', 1)[0]
    try:
        os.mkdir(dirname)
    except:
        pass
    f.close()
    tables = []
    ttags = soup.findAll('table')
    for t in ttags:
        tables.append([t['id'], t['caption'] if t.has_key('caption') else ""])
        tfilename = t['id']+ '.tsv'
        f = open(dirname + '/' + tfilename, 'w')
        tfields = t.find('fields').findAll('field')
        keys = []
        for k in tfields:
            keys.append(k['name'])
        s = '\t'.join(keys) + '\n'
        f.write(s.encode('utf8'))
        data = t.find('data')
        if data is not None:
            trows = data.findAll('row')
            for k in trows:
                elems = k.findAll('el')
                els = []
                for e in elems:
                    els.append(e.string.replace('\n', ' ').replace('\r', ' '))
                s = '\t'.join(els) + '\n'
                f.write(s.encode('utf8'))
        f.close()




if __name__ == "__main__":
    xml2csv(sys.argv[1])