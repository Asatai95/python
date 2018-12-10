import os
import sys
from PIL import Image
from django import *
from django.conf import settings
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.template import loader
from django.views.generic import CreateView, ListView
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect, render, resolve_url
from django.views import View, generic
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView,
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
)

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib import messages

from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.core.signing import BadSignature, SignatureExpired, loads, dumps
from django.http import Http404, HttpResponseBadRequest
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST

from .forms import (
    LoginForm, UserCreateForm, MyPasswordChangeForm, MyPasswordResetForm, MySetPasswordForm,
    UserUpdateForm
)

"""
Settingファイル
"""
from config.settings import *

"""
データベース
"""
Get_user = get_user_model()


"""
ログイン機能
"""
class Login(LoginView):

    form_class= LoginForm
    template_name = 'register/login.html'

"""
ログアウト機能
"""

class Logout(LogoutView):

    def get(self, request, *args, **kwargs):

        return redirect('register:login')


"""
ユーザー登録
"""

class UserCreate(generic.CreateView):
    """ユーザー仮登録"""
    template_name = 'register/user_create.html'
    form_class = UserCreateForm

    def form_valid(self, form):
        """仮登録と本登録用メールの発行."""
        # 仮登録と本登録の切り替えは、is_active属性を使うと簡単です。
        # 退会処理も、is_activeをFalseにするだけにしておくと捗ります。
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        # アクティベーションURLの送付
        current_site = get_current_site(self.request)
        domain = current_site.domain
        context = {
            'protocol': self.request.scheme,
            'domain': domain,
            'token': dumps(user.pk),
            'user': user,
        }

        subject = 'テスト'

        message_template = get_template('register/mail_template/create/message.txt')
        message = message_template.render(context)

        user.email_user(subject, message)
        return redirect('/user_create/done/')



class UserCreateDone(generic.TemplateView):
    """ユーザー仮登録したよ"""
    template_name = 'register/user_create_done.html'


class UserCreateComplete(generic.TemplateView):
    """メール内URLアクセス後のユーザー本登録"""
    template_name = 'register/user_create_complte.html'
    timeout_seconds = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS', 60*60*24)  # デフォルトでは1日以内

    def get(self, request, **kwargs):
        """tokenが正しければ本登録."""
        token = kwargs.get('token')
        try:
            user_pk = loads(token, max_age=self.timeout_seconds)

        # 期限切れ
        except SignatureExpired:
            return HttpResponseBadRequest()

        # tokenが間違っている
        except BadSignature:
            return HttpResponseBadRequest()

        # tokenは問題なし
        else:
            try:
                user = Get_user.objects.get(pk=user_pk)
            except Get_user.DoesNotExist:
                return HttpResponseBadRequest()

            if not user.is_active:
                # 問題なければ本登録とする
                user.is_active = True
                user.save()

                return super().get(request, **kwargs)

        return HttpResponseBadRequest()

class PasswordChange(PasswordChangeView):
    """パスワード変更ビュー"""
    form_class = MyPasswordChangeForm
    success_url = reverse_lazy('register:password_change_done')
    template_name = 'register/password_change.html'


class PasswordChangeDone(PasswordChangeDoneView):
    """パスワード変更しました"""
    template_name = 'register/password_change_done.html'


"""
パスワード再設定
"""
class PasswordReset(PasswordResetView):
    """パスワード変更用URLの送付ページ"""

    subject_template_name = 'register/mail_template/password_reset/subject.txt'
    email_template_name = 'register/mail_template/password_reset/message.txt'
    template_name = 'register/password_reset_form.html'
    form_class = MyPasswordResetForm
    success_url = reverse_lazy('register:password_reset_done')


class PasswordResetDone(PasswordResetDoneView):
    """パスワード変更用URLを送りましたページ"""
    template_name = 'register/password_reset_done.html'


class PasswordResetConfirm(PasswordResetConfirmView):
    """新パスワード入力ページ"""
    form_class = MySetPasswordForm
    success_url = reverse_lazy('register:password_reset_complete')
    template_name = 'register/password_reset_confirm.html'


class PasswordResetComplete(PasswordResetCompleteView):
    """新パスワード設定しましたページ"""
    template_name = 'register/password_reset_complete.html'

"""
個人のみ、閲覧可能（バリデーション）
"""
class PermissionsMypage(UserPassesTestMixin):

    raise_exception = True

    def test_func(self):
        user = self.request.user

        return user.pk == self.kwargs['pk'] or user.is_superuser

"""
マイページ
"""
class UserDetail(PermissionsMypage, generic.DetailView):
    model = Get_user
    template_name = 'register/user_detail.html'


"""
マイページ更新
"""
class UserUpdate(PermissionsMypage, generic.UpdateView):
    model = Get_user
    form_class = UserUpdateForm
    template_name = 'register/user_form.html'

    def get_success_url(self):

        User = Get_user.objects.all().filter(pk=self.kwargs['pk'])
        img_file = self.request.FILES['img_file'].name
        img_filename = Image.open(self.request.FILES['img_file'])
        img_filename.save(os.path.join('./media/img/', img_file))

        img_file = os.path.join('/media/img/', img_file)
        for user in User:
            user.image = user
        user.image = img_file
        user.save()

        return resolve_url('register:user_detail', pk=self.kwargs['pk'])

"""
TOPページ View
"""
class Main(View):

    template_name = 'apps/index.html'

    def get(self, request, *args, **kwargs):

        return render(request, self.template_name)
