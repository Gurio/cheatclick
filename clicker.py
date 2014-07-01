#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import urllib
import cookielib
import json
import sys

def get_html (data):
	req = urllib2.Request('http://www.eda.by/enter.php', data)
	response = urllib2.urlopen(req)
	return response.read().decode('cp1251').encode('utf8')

with open('./exceptions', 'a') as excepts, open('./log', 'a') as log:
	#cj = cookielib.MozillaCookieJar()
	#cj.load('./cookies.txt') 

	opener = urllib2.build_opener()#urllib2.HTTPCookieProcessor(cj))
	opener.addheaders = [	
							('Accept-Language', 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4,be;q=0.2'),
							('Connection', 'keep-alive'),
							('Content-Length','15'),
							('Content-Type', 'application/x-www-form-urlencoded'),
							('Cookie', 'PHPSESSID=fen1abk47dct0v6s4ol6c103e5; mobile=n; __utma=125156309.1557815832.1403775274.1403792281.1404116627.4; __utmc=125156309; __utmz=125156309.1403775274.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _ym_visorc_543098=w; __utmb=125156309.15.10.1404116627; eda=broadcast.field%40gmail.com%3A5KykUWhXUTk0Y'),
							('Host','www.eda.by'),
							('Origin', 'http://www.eda.by'),
							('Referer', 'http://www.eda.by/my/history/'),
							('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-GB; rv:1.9.2.13) Gecko/20101203 Firefox/3.6.13')]
	urllib2.install_opener(opener)

	lag = 5
        p_type = ["11","12","13","14"]
        finish_clicks = [x-lag for x in [500, 350, 250, 150]]

	fetch_val = {'act' : 'getcrazy'} 

	post_val = [[('act', 'crazyg'), ('r', p_type[0])],
				[('act', 'crazyg'), ('r', p_type[1])],
				[('act', 'crazyg'), ('r', p_type[2])]] # act:crazyg r:11,12,13

	fetch_data = urllib.urlencode(fetch_val)
	post_data = [urllib.urlencode(x) for x in post_val]

	print fetch_data
	print post_data
	log.write('LOG\n')
	log.write(get_html(post_data[0])+'\n')
	log.write(get_html(fetch_data)+'\n')
	log.flush()
	while True:
		try:
			html = get_html(fetch_data)
			jdata = json.loads(html)
			#print jdata
			for x in xrange(len(p_type)):
				#print int(jdata[p_type[x]]['tek']), finish_clicks[x] 
				if int(jdata[p_type[x]]['tek']) >= finish_clicks[x]:
					log.write(get_html(post_data[x])+'\n')
					log.write(get_html(fetch_data)+'\n')
					log.write(get_html(post_data[x])+'\n')
					log.flush()
					break
		except:
			excepts.write("Except: ")
			excepts.write(html+'\n')
			excepts.flush()
		else:
			pass