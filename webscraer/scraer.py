# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import urllib2
from bs4 import BeautifulSoup
import re

if __name__ == '__main__':
	content0 = urllib2.urlopen(r'http://music.douban.com/').read()
	soup = BeautifulSoup(content0)
	list0 = soup.find('ul', {'id': 'newcontent0'}).findAll('li', {'class': 'clearfix'})
	list1 = []
	for tag in list0:
		str0 = tag.find('h3').find('a').text
		str1 = tag.find('div', {'class': 'star clearfix'}).text
		list1.append([str0, str1])
	for d in list1:
		# 如果歌曲评分超过8.5，推荐给我
		if float(d[1]) >= 8.5:
			# 以发送邮件形式通知我
			# TODO
			print(d[0])
