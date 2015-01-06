# -*- coding: utf-8 -*-
import os
# 切换至项目根目录
project = os.path.split(os.path.realpath(__file__))[0]
os.chdir(project)
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import urllib2
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
smtp = smtplib.SMTP()

if __name__ == '__main__':
    content0 = urllib2.urlopen(r'http://music.douban.com/').read()
    soup = BeautifulSoup(content0)
    list0 = soup.find('ul', {'id': 'newcontent0'}).findAll('li', {'class': 'clearfix'})
    list1 = []
    for tag in list0:
        str0 = tag.find('h3').find('a').text
        str1 = tag.find('div', {'class': 'star clearfix'}).text
        list1.append([str0, str1])
    content = ''
    for d in list1:
        # 如果歌曲评分超过8.5，推荐给我
        if float(d[1]) > 8.5:
            # 以发送邮件形式通知我
            content += d[0] + '\t' + d[1] + ';'
    smtp.connect('smtp.126.com')
    msg = MIMEText(content, 'html', 'utf-8')
    msg['From'] = 'heavenfox@126.com'
    msg['To'] = '1553556149@qq.com'
    msg['Subject'] = 'Notify new music from DouBan'
    smtp.login('heavenfox@126.com', 'asd123,./asd')
    smtp.sendmail('heavenfox@126.com', '1553556149@qq.com', msg.as_string())
    smtp.quit()