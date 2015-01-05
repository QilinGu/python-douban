# -*- coding: gbk -*-
import sys
reload(sys)
sys.setdefaultencoding('gbk')
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
		list1.append([str0])
	for d in list1:
		print d[0]