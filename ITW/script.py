import os
import sys
import datetime as dt
import time
import smtplib
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ITW.settings')
django.setup()

from django.contrib.auth.models import User
from app.models import Event

event_list = list(Event.objects.order_by('start_time'))
user_list = list(User.objects.all())
user_list = list(User.objects.order_by('last_login'))



for i in event_list:
     def send_email(receiver_email):
         email_user = 'agrecormobo1@gmail.com'
         server = smtplib.SMTP ('smtp.gmail.com', 587)
         server.starttls()
         server.login(email_user, 'IaaKn!120')

         #EMAIL
         message = i.title
         server.sendmail(email_user, receiver_email, message)
         server.quit()
     print('hello')
     send_time = dt.datetime(i.start_time.year,i.start_time.month,i.start_time.day,i.start_time.hour,i.start_time.minute,0)
     if send_time.timestamp() - time.time() < 0 :
         print('sorry')
         continue
     else:
         time.sleep(send_time.timestamp() - time.time())
         send_email(i.user.email)
         print('email sent')
