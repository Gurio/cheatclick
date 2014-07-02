#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gevent
from gevent import monkey

monkey.patch_all()

import urllib2
import urllib
import cookielib
import socket
import datetime
import json
import sys

sh_num = int(sys.argv[1])

ip_addresses = ['104.131.229.138', '107.170.12.7', '107.130.112.57', '105.124.112.71']

true_socket = socket.socket
def make_socket(addr):
	def bound_socket(*a, **k):
	    sock = true_socket(*a, **k)
	    sock.bind((addr, 0))
	    return sock
	return bound_socket

	#socket.socket = make_socket()

def open_with_ip (url, data, opener, addr):
	#print "open"
	#socket.socket = make_socket(addr)	
	#print 'by', addr
	return opener.open('http://www.eda.by/enter.php', data)
	#to_ret = urllib2.urlopen('http://httpbin.org/ip')
	#print to_ret
	#socket.socket = true_socket	
	

def get_html (data, openers=None):
	if openers:
		response = openers[sh_num].open('http://www.eda.by/enter.php', data)#open_with_ip('http://www.eda.by/enter.php', data, openers[sh_num], ip_addresses[sh_num])
		return [str(datetime.datetime.utcnow()) + ' ' + str(response.read().decode('cp1251').encode('utf8')) + '\n']
	else:
		req = urllib2.Request('http://www.eda.by/enter.php', data)
		response = urllib2.urlopen(req)
		return response.read().decode('cp1251').encode('utf8')
	
def make_opener (cookie):
	opener = urllib2.build_opener()#urllib2.HTTPCookieProcessor(cj))
	opener.addheaders = [	
							('Accept-Language', 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4,be;q=0.2'),
							('Connection', 'keep-alive'),
							('Content-Length','15'),
							('Content-Type', 'application/x-www-form-urlencoded'),
							('Cookie', cookie),
							('Host','www.eda.by'),
							('Origin', 'http://www.eda.by'),
							('Referer', 'http://www.eda.by/my/history/'),
							('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-GB; rv:1.9.2.13) Gecko/20101203 Firefox/3.6.13')]
	return opener
	
with open('./exceptions', 'a') as excepts, open('./log', 'a') as log:
	#cj = cookielib.MozillaCookieJar()
	#cj.load('./cookies.txt') 
	cookies_list = ['PHPSESSID=fen1abk47dct0v6s4ol6c103e5; mobile=n; __utma=125156309.1557815832.1403775274.1403792281.1404116627.4; __utmc=125156309; __utmz=125156309.1403775274.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _ym_visorc_543098=w; __utmb=125156309.15.10.1404116627; eda=broadcast.field%40gmail.com%3A5KykUWhXUTk0Y',
'mobile=n; __utma=125156309.1557815832.1403775274.1404203947.1404211604.10; __utmz=125156309.1403775274.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); eda=re.stage00101%40gmail.com%3A5Kdtf5thaZG42; PHPSESSID=agunapj56kgm6a5lq79g2dn2u1; __utmc=125156309',
'mobile=n; eda=lopatsina%40yandex.by%3A5K1ZBrEeF5n3s; PHPSESSID=b5a9m6ltv8m2fmoln6r230bjh6; _ym_visorc_543098=w; __utma=125156309.1676049902.1404062398.1404132383.1404158777.5; __utmb=125156309.2.9.1404158778305; __utmc=125156309; __utmz=125156309.1404062398.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
'mobile=n; PHPSESSID=1upqr8rq7j0jkvvv2a30gq63e4; eda=Mashabububu%40gmail.com%3A5K7fepSQ4yhMo; _ym_visorc_543098=w; __utma=125156309.1676049902.1404062398.1404223725.1404237053.7; __utmb=125156309.5.9.1404237080411; __utmc=125156309; __utmz=125156309.1404062398.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)']
	openers = [make_opener(x) for x in cookies_list]#urllib2.HTTPCookieProcessor(cj))
	
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
	[log.write(x) for x in get_html(post_data[0], openers)]
	log.write(get_html(fetch_data))
	log.flush()
	while True:
		try:
			html = get_html(fetch_data)
			jdata = json.loads(html)
			#print jdata
			for x in xrange(len(p_type)):
				#print int(jdata[p_type[x]]['tek']), finish_clicks[x] 
				if int(jdata[p_type[x]]['tek']) >= finish_clicks[x]:
					[log.write(h) for h in get_html(post_data[x], openers)]
					log.write(get_html(fetch_data))
					[log.write(h) for h in get_html(post_data[x], openers)]
					log.flush()
					break
		except Exception as e:
			excepts.write(str(datetime.datetime.utcnow()) + ' ' + "Except: ")
			excepts.write(str(e.message) + str(e.args) +'\n')
			excepts.write(html+'\n')
			excepts.flush()
		else:
			pass
