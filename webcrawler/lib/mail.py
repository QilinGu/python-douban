# -*- coding: utf-8 -*-

from email.mime.text import MIMEText
import smtplib
from tool import dataserialization

f = open('conf/mailnotify.json')
json_manager = dataserialization.DataSerialization().json_to_data(f.read())
f.close()


class MailSender():
    def __init__(self):
        self.mail_host = json_manager.get('host_conf').get('mail_host')
        self.mail_user = json_manager.get('host_conf').get('mail_user')
        self.mail_passwd = json_manager.get('host_conf').get('mail_passwd')
        self.mail_from = json_manager.get('mail_conf').get('from')

    def send_mail(self, mail_to, mail_subject, mail_content):
        msg = MIMEText(mail_content, 'html', 'utf-8')
        msg['From'] = self.mail_from
        msg['To'] = mail_to
        msg['Subject'] = mail_subject
        s = smtplib.SMTP()
        s.connect(self.mail_host)
        s.login(self.mail_user, self.mail_passwd)
        s.sendmail(self.mail_from, mail_to, msg.as_string())
        s.quit()
