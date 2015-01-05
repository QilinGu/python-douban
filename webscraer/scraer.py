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
	list0 = soup.find('ul', {'id': 'newcontent0'})
	list2 = list0.findAll('li', {'class': 'clearfix'})
	list3 = list()
	for tag in list2:
		str0 = tag.find('h3').find('a').text.encode('gbk', 'ignore')
		print str0
		list3.append([str0])
	print(list3)