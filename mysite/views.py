from django.http import HttpResponse
from django.views.generic.edit import CreateView
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect, render
from django.views import View
from django.urls import reverse

import requests

"""
クッキー設定
"""
from django.template.loader import render_to_string
from django.http import HttpResponse
import datetime

"""
ライブラリ
"""
from mysite.library import *

"""
modelsファイル
"""
from mysite.models.user import *

"""
Index View(テスト画面)
"""
class IndexView(View):

    template_name = 'index.html'

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

    # def post(self, request, *args, **kwargs):
    #
    #     return redirect("/login/")

Register = Register.as_view()

"""
登録確認画面
"""
class Confirm(CreateView):

    template_name = 'sign.html'

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

        users_create(request.POST)

        """
        クッキー
        """

        login_user(user['name'])

        return login_user

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

        if login_form is False:

            not_match = 'Email、またはパスワードの入力内容が異なります'
            error = {
               'error': not_match
            }

            return render(request, self.template_name, error)
        else:

            """
            クッキー
            """

            response = redirect('/mypage/')
            response.set_cookie(key='cookie', value=user['name'], max_age=None, path='/')

            return redirect('/users/mypage/')

Login = Login.as_view()

"""
マイページ
"""

class Mypage(View):

    template_name = 'mypage.html'

    def get(self, request, *args, **kwargs):

        return render(request, self.template_name)

Mypage = Mypage.as_view()
