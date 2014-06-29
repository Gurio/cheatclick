#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import urllib
import json
import sys

def get_html (data):
	req = urllib2.Request('http://www.eda.by/enter.php', data)
	response = urllib2.urlopen(req)
	return response.read().decode('cp1251').encode('utf8')

excepts=open('./exceptions', 'w+')
log=open('./log', 'w+')

opener = urllib2.build_opener()
opener.addheaders.append(('Cookie', 'PHPSESSID=0skelcnh9k4fkrqcagf8gert37; mobile=n; eda=re.stage00101%40gmail.com%3A5Kdtf5thaZG42; __utma=125156309.2112618792.1404036061.1404036061.1404046268.2; __utmb=125156309.1.10.1404046268; __utmc=125156309; __utmz=125156309.1404036061.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _ym_visorc_543098=w'))

p_type = ["11","12","13","14"]
finish_clicks = [498, 348, 248, 148]

fetch_val = {'act' : 'getcrazy'} 

post_val = [[('act', 'crazyg'), ('r', p_type[0])],
			[('act', 'crazyg'), ('r', p_type[1])],
			[('act', 'crazyg'), ('r', p_type[2])]] # act:crazyg r:11,12,13

fetch_data = urllib.urlencode(fetch_val)
post_data = [urllib.urlencode(x) for x in post_val]

print fetch_data
print post_data

while True:
	try:
		html = get_html(fetch_data)
		jdata = json.loads(html)
		#print jdata
		for x in xrange(len(p_type)):
			#print int(jdata[p_type[x]]['tek']), finish_clicks[x] 
			if int(jdata[p_type[x]]['tek']) >= finish_clicks[x]:
				log.write(get_html(post_data[x]))
				log.write(get_html(fetch_data))
				log.write(get_html(post_data[x]))
				break
	except:
		excepts.write("Except!!!")
		excepts.write(html)
	else:
		pass
