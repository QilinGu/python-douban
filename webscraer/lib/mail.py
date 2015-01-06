# -*- coding: utf-8 -*-
from email.mime.text import MIMEText
import smtplib

class MailSender():
    def __init__(self):
        pass

    def send_mail(self, mail_from, mail_to, mail_subject, mail_content):
        smtp = smtplib.SMTP()
        smtp.connect()