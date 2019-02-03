import os
import sys

from django import *
from PIL import Image
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpRequest
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
import urllib3

from models.social import *
from models.user_auth import *
from django.db import models
from mysite.models import Article, RoomImage, Fab, ArticleRoom, ArticleFloor, ArticleLive, ArticleCreate
from django.contrib.auth import get_user_model

import requests

User = get_user_model()

"""
Google, ログイン認証
"""
from httplib2 import Http
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from apiclient.discovery import build
import hmac
import hashlib

SCOPE = 'https://www.googleapis.com/auth/plus.profile.emails.read'

flow = flow_from_clientsecrets(
   './client_id.json',
   scope=SCOPE,
   redirect_uri= "http://localhost:8000/auth/complete/google-oauth2/")

"""
facebook
# """
# FACEBOOK_ID = '292183621408680'
# FACEBOOK_SECRET = '1077fcc7e686d3c4ff08fbb05fcc94ab'
# FACEBOOK_CALLBACK_URL = 'http://localhost:8000/callback/facebook'

"""
Settingファイル
"""
sys.path.append(os.getcwd())
from config.settings import *

"""
imgファイル保存
"""
UPLOAD_FOLDER = '/static/img/'

"""
SNSログイン
"""

def create_socials_user(data):

    user_name = data["displayName"].replace(" ", "").replace("%20", "")

    secret = 'google'
    password = hmac.new(
                secret.encode('UTF-8'),
                SECRET_KEY.encode('UTF-8'),
                hashlib.sha256
           ).hexdigest()

    user = User.objects.create(
        username = user_name,
        email = data["emails"][0]['value'],
        password = password,
        is_staff = 0,
        is_active = 1,
        image='/static/img/profile.png',
    )

    if user:
        user.save()

        return user
    else:
        return redirect("apps:login")


def create_facebook_user(data):

    user_name = data["name"].replace(" ", "").replace("%20", "")

    secret = 'facebook'
    password = hmac.new(
                secret.encode('UTF-8'),
                SECRET_KEY.encode('UTF-8'),
                hashlib.sha256
           ).hexdigest()

    user = User.objects.create(
        username = user_name,
        email = data['email'],
        password = password,
        is_staff = 0,
        is_active = 1,
        image='/static/img/profile.png',
    )

    if user:
        user.save()

        return user
    else:
        return redirect("apps:login")

def create_socials(user_id , data, provider):
    if provider == 'google':
        social = Social(
           user_id = user_id,
           provider = provider,
           provider_id = data['id']
        )
    elif provider == 'facebook':
        social = Social(
           user_id = user_id.id,
           provider = provider,
           provider_id = data['id']
        )

    session.add(social)
    session.commit()

def check_socials(data, provider):

    if provider == 'google':
        social = session.query(Social).filter(
                    Social.provider == 'google',
                    Social.provider_id == data
                ).first()
    elif provider == 'facebook':
        social = session.query(Social).filter(
                    Social.provider == 'facebook',
                    Social.provider_id == data['id']
                ).first()

    if social is None:
        return False
    else:
        return social

"""
Facebook, ログイン認証
"""

def get_facebook_user(facebook_id):

    user = session.query(UserAuth).join(
             Social, UserAuth.id == Social.user_id
          ).filter(
             Social.provider_id == facebook_id
          ).first()
    return user.id

def get_facebook_access_token(code):

    url = 'https://graph.facebook.com/v3.2/oauth/access_token'
    params = {
            'redirect_uri': FACEBOOK_CALLBACK_URL,
            'client_id': SOCIAL_AUTH_FACEBOOK_KEY,
            'client_secret': SOCIAL_AUTH_FACEBOOK_SECRET,
            'code': code,
    }
    r = requests.get(url, params=params)
    print(r)
    return r.json()['access_token']

def check_facebook_access_token(access_token):

    url = 'https://graph.facebook.com/debug_token'
    params = {
        'input_token': access_token,
        'access_token': '%s|%s' % (SOCIAL_AUTH_FACEBOOK_KEY, SOCIAL_AUTH_FACEBOOK_SECRET)
    }
    r = requests.get(url, params=params)
    return r.json()['data']

def get_facebook_user_info(access_token, user_id):

    url = 'https://graph.facebook.com/%s' % (user_id)
    params = {
        'fields': 'name, email',
        'access_token': access_token,
    }
    return requests.get(url, params=params).json()

"""
Google, ログイン認証
"""

def google_login_flow(code):


    credentials = flow.step2_exchange(code)

    CREDENTIALS_FILE = "./credentials"
    Storage(CREDENTIALS_FILE).put(credentials)

    credentials = Storage(CREDENTIALS_FILE).get()
    http_auth = credentials.authorize(Http())
    service = build('plus', 'v1', http=http_auth)

    result = service.people().get(userId='me').execute()

    return result

