from django import *
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import CreateView, ListView
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect, render
from django.views import View
from django.urls import reverse
from django.contrib.auth.decorators import login_required

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

import requests

"""
ライブラリ
"""
from mysite.library import *

"""
modelsファイル
"""
from mysite.models.user import *

class Indexhome(View):

    template_name = 'index.html'

    def get(self, request, *args, **kwargs):

        return render(request, 'index.html')

home = Indexhome.as_view()

"""
Index View(テスト画面)
"""
class IndexView(View):

    template_name = 'index.html'
    @login_required
    def get(self, request, *args, **kwargs):

        return render(request, self.template_name)

Index = IndexView.as_view()

"""
ユーザー登録
"""
class Register(CreateView):

    template_name = 'sign.html'

    def get(self, request, *args, **kwargs):

        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):

        """
        クッキー
        """
        user = login_user_cookie()
        cookie = login_user(user)

        return cookie


Register = Register.as_view()

"""
登録確認画面
"""
class Confirm(CreateView):

    template_name = 'new_confirm.html'
    template_name_error = 'sign.html'

    def get(self, request, *args, **kwargs):

        user = check_form(request.POST)

        return user

    def post(self, request, *args, **kwargs):

        user = check_form(request.POST)

        mail = check_email(request.POST)
        if mail is False:
            duplicate_error = 'すでに使用されているEmail('+request.POST.get('email')+')アドレスです'
            error = {
               'error': duplicate_error
            }

            return render(request, self.template_name, error)

        user = check_form(request.POST)
        users_create(request.POST)

        return render(request, template_name, user)

Confirm = Confirm.as_view()

"""
ログイン画面
"""
class Login(View):

    template_name = 'login.html'

    def get(self, request, *args, **kwargs):

        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):

        login_form = user_login(request.POST)

        user = login_user_checker(request.POST)

        if login_form == None:

            """
            クッキー
            """
            cookie = login_user(user)

            return cookie

        else:

            return render(request, self.template_name, login_form['error'])

Login = Login.as_view()

"""
マイページ
"""

class Mypage(View):

    template_name = 'mypage.html'

    def get(self, request, *args, **kwargs):

        return render(request, self.template_name)

Mypage = Mypage.as_view()

"""
google、ログイン機能
"""

class GoogleLogin(View):

    def get(self, request, *args, **kwargs):

        SCOPE = 'https://www.googleapis.com/auth/plus.login'

        flow = flow_from_clientsecrets(
           './client_id.json',
           scope=SCOPE,
           redirect_uri= "http://127.0.0.1:8000/auth/complete/google-oauth2/")

        auth_uri = flow.step1_get_authorize_url()

        return redirect(auth_uri)

GoogleLogin = GoogleLogin.as_view()

"""
google、CallBack
"""

class GoogleCallBack(View):

    def get(self, request, *args, **kwargs):

        if request.GET.get('code'):
            data = google_login_flow(request.GET.get('code'))
            check = check_socials(data['id'], 'google')
            if check is not False:
                social = session.query(User).join(
                         Social, User.id == Social.user_id).filter(
                         Social.provider == 'google',
                         Social.provider_id == data['id']).first()

                if social:
                    cookie = login_user(social.id)
                    return cookie
                else:
                    pass
            else:
                user = create_socials_user(data)
                create_socials(user.id, data, 'google')
                cookie = login_user(user.id)
                return cookie
        else:
            return redirect('/login/')

GoogleCallBack = GoogleCallBack.as_view()

"""
Facebook, ログイン認証
"""

class FacebookLogin(View):

    def get(self, request, *args, **kwargs):
        url = 'https://www.facebook.com/dialog/oauth/'

        params = {
            'response_type': 'code',
            'redirect_uri': config.settings.FACEBOOK_CALLBACK_URL,
            'client_id': config.settings.FACEBOOK_ID
        }

        redirect_url = requests.get(url, params=params).url
        return redirect(redirect_url)

FacebookLogin = FacebookLogin.as_view()

"""
Facebook, CallBack
"""

class FacebookCallBack(View):

    def get(self, request, *args, **kwargs):

        try:
            if request.GET.get('code'):
                access_token = get_facebook_access_token(request.GET.get('code'))
                data = check_facebook_access_tokn(access_token)
                if data['is_valid']:
                    data = get_facebook_user_info(access_token, data['user_id'])
                    if check_socials(data, 'facebook'):
                        login_user(user.id)
                        return redirect('/users/mypage/')

                    else:
                        user = create_facebook_user(data)
                        create_socials(user, data, 'facebook')
                        login_user(user.id)
                        return redirect('/users/mypage/')
                else:
                    return redirect('/login/')

        except:
            return redirect('/login/')

FacebookCallBack = FacebookCallBack.as_view()

"""
ログアウト機能
"""

class Logout(View):

    def get(self, request, *args, **kwargs):
        log = logout()

        return log
Logout = Logout.as_view()
