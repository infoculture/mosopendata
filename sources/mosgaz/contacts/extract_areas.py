#!/usr/bin/env python

import urllib2
from BeautifulSoup import BeautifulSoup
import json
from StringIO import StringIO

URL = 'http://www.mos-gaz.ru/services/territory/ajax_manag.php?ID='


def convert_table(tag):
	rows = []
	table = tag.find('table')
	if not table:
		return None
	for r in table.findAll('tr', recursive=False):
		rowdata = []
 		children = r.findAll('td', recursive=False)
		for c in children:
			rowdata.append(c.string)
		rows.append(rowdata)
	return rows


f = open('data/mosgaz_areas.json', 'r')
data = f.read()
f.close()
jdata = json.loads(data)


io = StringIO()
io.write(('\t'.join(['areaid', 'areaname', 'orgname', 'fieldtype', 'value', 'value_descr'])).encode('utf8')+'\n')
for datarow in jdata['rows']:
	id = datarow['areaid']
	print "Extracting data", id
	u = urllib2.urlopen(URL + id)
	data = u.read()
	u.close()
	print "Saving data", id
	f = open('data/pages/%s.html' % id, 'w')
	f.write(data)
	f.close()
	soup = BeautifulSoup(data)
	tables = soup.findAll('table', attrs={'class': 'vacTable'})
	for t in tables:
		orgname = t.parent.parent.previous.previous.previous
		allrowdata = []
 		rows = t.findAll('tr', recursive=False)
 		for r in rows:
# 			rowdata = []
 			rowtype = 'kv'
 			children = r.findAll('td', recursive=False)
 			if len(children) == 0:
 				continue
 			if children[0]['class'] == 'a':
 				if children[1].string is not None:
 					rowdata = [id, datarow['area'], orgname, children[0].string, children[1].string, '']
					io.write(('\t'.join(rowdata)).encode('utf8')+'\n')
 				else:
# 					rowdata = [children[0].string, ]
 					innertab = convert_table(children[1])
					if innertab is not None:
	 					for rowdata in innertab:
 							fullrow = [id, datarow['area'], orgname, unicode(children[0].string)]
 							fullrow.extend(rowdata)
 							frow = map(unicode, fullrow)
							io.write(('\t'.join(frow)).encode('utf8')+'\n')
 			elif children[0]['class'] == 'ab':
 				p = children[0].find('p')
 				if p is not None: 
#	 				rowdata = [orgname, 'description', p.prettify().decode('utf8'), '']
#					io.write(('\t'.join(rowdata)).encode('utf8')+'\n')
					pass
	 			else:
	 				a = children[0].find('a')
	 				if a is not None:
		 				rowdata = [id, datarow['area'], orgname, 'url', 'http://www.mos-gaz.ru' + a['href'], '']
						io.write(('\t'.join(rowdata)).encode('utf8')+'\n')
					else:
						continue
			allrowdata.append(rowdata)
f = open('data/allorgs.tsv', 'w')
f.write(io.getvalue())
f.close()
		