from django.http import HttpResponse
from django.views.generic.edit import CreateView
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect, render
from django.views import View
from django.urls import reverse

import requests

"""
ライブラリ
"""
from mysite.library import *

"""
modelsファイル
"""
from mysite.models.user import *

"""
Index View
"""
class IndexView(View):
    def get(self, request, *args, **kwargs):

        return render(request, 'index.html')

Index = IndexView.as_view()

"""
Sign up
"""
class Register(CreateView):

    def get(self, request, *args, **kwargs):

        return render(request, 'sign.html')

    def post(self, request, *args, **kwargs):

        return redirect("/login/")

Register = Register.as_view()

"""
登録確認画面
"""
class Confirm(CreateView):

    def post(self, request, *args, **kwargs):
        user = check_form(request.POST)
        user_form = {
            'name': user.name,
            'email': user.email,
            'password': user.password,
        }

        mail = check_email(request.POST)
        if mail is False:
            duplicate_error = 'すでに使用されているEmail('+request.POST.get('email')+')アドレスです'
            error = {
               'error': duplicate_error
            }

            return render(request, 'sign.html', error)

        users_create(request.POST)

        return render(request, 'new_confirm.html', user_form)

Confirm = Confirm.as_view()

"""
ログイン画面
"""
class Login(View):
    def get(self, request, *args, **kwargs):

        return render(request, 'login.html')

    def post(self, request, *args, **kwargs):

        login_form = user_login(request.POST)

        if login_form is False:

            not_match = 'Email、またはパスワードの入力内容が異なります'
            error = {
               'error': not_match
            }

            return render(request, 'login.html', error)
        else:

            return redirect('/users/mypage/')

Login = Login.as_view()

"""
マイページ
"""

class Mypage(View):
    def get(self, request, *args, **kwargs):

        return render(request, 'mypage.html')

Mypage = Mypage.as_view()
