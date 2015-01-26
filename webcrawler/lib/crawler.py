# -*- coding: utf-8 -*-
import urllib2
from bs4 import BeautifulSoup
from tool.dataserialization import DataSerialization
from mail import MailSender
f = open('conf/mailnotify.json')
serialization = DataSerialization()
json_manager = serialization.json_to_data(f.read())
f.close()


class Crawler():
    def __init__(self):
        self.mail_to = json_manager.get('mail_conf').get('to')
        self.subject = json_manager.get('mail_conf').get('subject')

    def run(self):
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
        if content != '':
            print('今日推荐歌曲, 注意查收您的邮件!')
            mail_sender = MailSender()
            mail_sender.send_mail(self.mail_to, self.subject, content)
