from django import *

from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from config.settings import session

from mysite.models.user import *
from mysite.models.social import *

"""
Google, ログイン認証
"""
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from apiclient.discovery import build

"""
Settingファイル
"""
import config.settings

SCOPE = 'https://www.googleapis.com/auth/plus.login'

flow = flow_from_clientsecrets(
   './client_id.json',
   scope=SCOPE,
   redirect_uri= "http://127.0.0.1:8000/auth/complete/google-oauth2/")

"""
クッキーの設定
"""
def login_user_cookie():

    user = session.query(User).order_by(desc(User.created_at)).first()

    return user.id

def login_user(user_id):

    response = redirect('/users/mypage/')
    response.set_cookie(key='cookie', value=user_id, max_age= 360 * 24 * 365 * 2, path='/')

    return response

"""
クッキーの取得
"""

def get_cookie(request):

    user_name = request.COOKIE.get("value")
    if user_name:
        return session.query(User).get(user_name)
    else:
        return None

"""
ログインしていれば、リダイレクト
"""

def is_logged_in_redirect(user):
    if user is not None:
        return redirect('/index/')

"""
ユーザー登録確認画面用のチェック項目
"""

def check_form(form):

    user = User(
         name=form.get('name'),
         email=form.get('email'),
         password=form.get('password'),
    )

    user_form = {
         'id': user.id,
         'name': user.name,
         'email': user.email,
    }

    return user_form

"""
Emailの有、無
"""

def check_email(form):

    user_email_cheker = session.query(User).filter(
                            User.email == form.get('email'),
                        ).all()

    if user_email_cheker:
        return False
    else:
        return True

"""
usersテーブル作成
"""

def users_create(form):

    user = User(
           name=form.get('name'),
           email=form.get('email'),
           password=form.get('password'),
    )

    session.add(user)
    session.commit()

    return user

"""
ログイン画面
"""

def user_login(form):

    mail = session.query(User).filter(
                User.email == form.get('email')
           ).first()

    if mail == None:
        error = {
            'error': 'メールアドレスの内容が異なります'
        }
        return error

    password = session.query(User).filter(
                  User.password == form.get('password')
               ).first()

    if password == None:
        error = {
            'error': 'パスワードの内容が異なります'
        }
        return error

def login_user_checker(form):

    user_name_check = session.query(User).filter(
            User.email == form.get('email')
          ).first()

    return user_name_check.id

"""
SNSログイン
"""

def create_socials_user(data):

    user = User(
        name = data['displayName'],
    )

    session.add(user)
    session.commit()

    return user

def create_facebook_user(data):

    user = User(
        name = data['name'],
    )

    session.add(user)
    session.commit()

    return user

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
    if social is None:
        return False
    else:
        login_user(social.user_id)
        return True

"""
facebook, ログイン認証
ユーザーID、ユーザー名取得
"""

def get_facebook_access_token(code):

    url = 'https://graph.facebook.com/v3.1/oauth/access_token'
    params = {
            'redirect_uri': config.settings.FACEBOOK_CALLBACK_URL,
            'client_id': config.settings.FACEBOOK_ID,
            'client_secret': config.settings.FACEBOOK_SECRET,
            'code': code,
    }
    r = requests.get(url, params=params)
    return r.json()['access_token']

def check_facebook_access_tokn(access_token):

    url = 'https://graph.facebook.com/debug_token'
    params = {
        'input_token': access_token,
        'access_token': '%s|%s' % (config.settings.FACEBOOK_ID, config.settings.FACEBOOK_SECRET)
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
google, ログイン認証
ユーザーID、ユーザー名の取得
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

"""
クッキーの削除、ログアウト
"""
def logout():

    response = redirect('/login/')
    response.delete_cookie(key='cookie')

    return response
