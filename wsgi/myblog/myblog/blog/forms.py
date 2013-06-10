# -*- coding: utf-8 -*-
from email.Header import make_header as mkh
import email
from email.Encoders import *
import base64
from email.MIMEText import MIMEText
from smtplib import SMTP
from django import forms
from django.conf import settings
from django.template.loader import render_to_string
from myblog.true_settings import *
from captcha.fields import CaptchaField
class FeedbackForm(forms.Form):
    email = forms.CharField(label=u'Ваш e-mail', max_length=200)
    topic = forms.CharField(label=u'Тема', max_length=200)
    response = forms.CharField(label=u'Что стряслось', max_length=500,
    widget=forms.Textarea(attrs={'rows': 5, 'cols': 30}))
    captcha = CaptchaField()
    def send_mail(self):
        # готовим контекст для сообщения
        response = self.cleaned_data['response']
        msg = MIMEText(response,_charset='utf-8')
        msg.preamble = "From blog"
        emaill = self.cleaned_data['email']
        subject = self.cleaned_data['topic']
        msg["Subject"] = mkh([(subject, "utf-8")])
        msg["From"] = mkh([("User_of_blog", "utf-8"), ("<%s>"%emaill, "us-ascii")])
        msg["To"] = mkh([("Admin", "utf-8"), ("<%s>"%admin_mail, "us-ascii")])
        msg = msg.as_string()
        message=msg
        toaddr = admin_mail
        fromaddr = fictive_mail 
        password = admin_mail_password 
        connection = SMTP('pop.rambler.ru',25)
        SMTP.login(connection,fromaddr,password)
        connection.sendmail(fromaddr,toaddr,message)
        connection.quit()
