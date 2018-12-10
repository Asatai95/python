from email.mime.text import MIMEText
import smtplib

import os, sys
sys.path.append(os.getcwd())
from config import settings


def Send_mail(to_email, send_type):

    # user_key = str(random.randrange(100))
    # key = hmac.new(
    #             user_key.encode('UTF-8'),
    #             settings.SECRET_KEY.encode('UTF-8'),
    #             hashlib.sha256
    #        ).hexdigest()

    body=''
    subject = ''
    url = "{{ protocol }}://{{ domain }}{% url 'password_reset_confirm' uidb64=uid token=token %}"
    if send_type == 'remake':
        body = '〇〇です。 \n\nパスワード再設定用のメールです \n\n'+url+''
        subject = '【パスワード再設定】〇〇〇〇〇'

    message = MIMEText(body)
    message['Subject'] = subject
    message['From'] = EMAIL_HOST_USER
    message['To'] = to_email

    sender = smtplib.SMTP_SSL(HOST_SMTP)
    sender.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
    sender.sendmail(EMAIL_HOST_USER, to_email, message.as_string())
    sender.quit()
