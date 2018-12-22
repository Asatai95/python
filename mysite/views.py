import os
import sys
from PIL import Image
from django import *
from django.conf import settings
from importlib import import_module
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.views.generic import CreateView, ListView, TemplateView
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect, render, resolve_url, render_to_response
from django.views.generic.edit import UpdateView
from django.views import View, generic
from django.urls import reverse


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
from django.db.models import Q
from mysite.models import Article, RoomImage, Fab, ArticleRoom, ArticleFloor, ArticleLive, ArticleCreate
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.core.signing import BadSignature, SignatureExpired, loads, dumps
from django.http import Http404, HttpResponseBadRequest
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST

from .forms import (
    LoginForm, UserCreateForm, MyPasswordChangeForm, MyPasswordResetForm, MySetPasswordForm,
    UserUpdateForm, Createform, LoginCustomerForm, ArticleUpdateForm
)

import requests

import re


"""
Settingファイル
"""
from config.settings import *
from mysite.library import *

"""
データベース
"""
Get_user = get_user_model()
ArticleMain = Article.objects.all()
ArticleImage = RoomImage.objects.all()


"""
エラーページ
"""

def error_404(request):

    contexts = {
        'request_url': request.path,
    }

    return render(request, '404.html', contexts, status=404)

def error_500(request):

    contexts = {
        'request_url': request.path,
    }

    return render(request, '500.html', contexts, status=500)


"""
ログインしていない場合、Loginページ
"""
class MyView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'apps/index.html'


"""
ログイン機能（ユーザー）
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
        img_file = os.path.join('/static/img/profile.png')
        user.image = img_file
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

    def get_context_data(self, **kwargs):

        context = super(IndexView, self).get_context_data(**kwargs)
        floor_list = ArticleFloor.objects.all().order_by('floor_id')
        room_list = ArticleRoom.objects.all().order_by('room_id')
        context['floor_list'] = floor_list
        context['room_list'] = room_list

        return context

    def get(self, request, **kwargs):

        tmp_fab = []
        tmp_article = []
        fab = Fab.objects.filter(user=request.user ,flag=1).values('article', 'updated_at')
        for tmp in fab:
            fab_dic = {'article': tmp['article'], 'updated': tmp['updated_at']}
            tmp_fab.append(fab_dic)

        article = ArticleMain.values('id', 'article_name', 'article_image', 'comments')
        for tmp in article:
            article_dic = {'id': tmp['id'], 'name': tmp['article_name'] ,'image': tmp['article_image'], 'comment': tmp['comments']}
            tmp_article.append(article_dic)

        return render(request, self.template_name, {'fab': tmp_fab, 'list': tmp_article})



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
        img_filename.save(os.path.join('./static/img/', img_file))

        img_file = os.path.join('/static/img/', img_file)
        for user in User:
            user.image = user
        user.image = img_file
        user.save()

        return resolve_url('register:user_detail', pk=self.kwargs['pk'])

"""
不適切な入力、トップページにリダイレクト
"""

def Redirect(request, location=None):

    return redirect('apps:top')


"""
個人のおすすめ項目
"""
class LoginAfter(generic.ListView):

    template_name = 'apps/login_after.html'

    def get(self, request, *args, **kwargs):

        if request.user.fab_selection_id:
            return redirect('apps:top')

        return render(request, 'apps/login_after.html')

    def post(self, request, *args, **kwargs):

        rent = request.POST.get('rent_selection_1')
        if rent == '':
            rent = request.POST.get('rent_selection_2')
        park = request.POST.get("park_selection_1")
        if park == '':
            park = request.POST.get("park_selection_2")

        if rent == '0' and park == '0':
            address = request.POST.get("address")
            tmp = '1' +','+ ''+address+''
            user_query = User.objects.filter(id=request.user.id)
            for user in user_query:
                user.fab_selection_id = tmp
                user.save()
        elif rent == '0' and park == '1':
            address = request.POST.get("address")
            tmp = '2' +','+ ''+address+''
            user_query = User.objects.filter(id=request.user.id)
            for user in user_query:
                user.fab_selection_id = tmp
                user.save()
        elif rent == '1' and park == '0':
            address = request.POST.get("address")
            tmp = '3' +','+ ''+address+''
            user_query = User.objects.filter(id=request.user.id)
            for user in user_query:
                user.fab_selection_id = tmp
                user.save()
        elif rent == '1' and park == '1':
            address = request.POST.get("address")
            tmp = '4' +','+ ''+address+''
            user_query = User.objects.filter(id=request.user.id)
            for user in user_query:
                user.fab_selection_id = tmp
                user.save()
        else:
            return redirect("apps:login_after")

        return redirect("apps:login_after")

"""
TOPページ, 検索機能
"""

class MainView(generic.ListView):
    model = Article
    template_name = 'apps/index.html'
    success_url = 'apps:top'

    def get_context_data(self, **kwargs):

        """
        トップ画面表示(一部)
        """

        context = super(MainView, self).get_context_data(**kwargs)
        user = User.objects.all().filter(id=self.request.user.id).order_by("fab_selection_id")
        floor_list = ArticleFloor.objects.all().order_by('floor_id')
        room_list = ArticleRoom.objects.all().order_by('room_id', 'room_live_id')
        fab_view = Fab.objects.all()

        """
        現在の日付取得、最新の記事情報を開示する
        """
        import datetime

        dt = datetime.datetime.utcnow()
        month_first = dt.date() - datetime.timedelta(days=dt.day - 1)
        today = datetime.date.today()
        fab_article = Article.objects.all().filter(created_at__range=(month_first, today))

        live = ArticleLive.objects.all()

        context['floor_list'] = floor_list
        context['room_list'] = room_list
        context['fab_view'] = fab_view
        context['live'] = live
        context['fab_article'] = fab_article

        """
        おすすめ表記
        """
        fab_selection_list = []
        for user_list in user:
            if '1' in user_list.fab_selection_id:
                user_fab = Article.objects.distinct().filter(
                       address__contains=user_list.fab_selection_id.replace("1,", ""), park="駐車場あり", rent__lte='5'
                )
            elif '2' in user_list.fab_selection_id:
                user_fab = Article.objects.distinct().filter(
                       address__contains=user_list.fab_selection_id.replace("2,", ""), park="駐車場なし", rent__lte='5'
                )
            elif '3' in user_list.fab_selection_id:
                user_fab = Article.objects.distinct().filter(
                       address__contains=user_list.fab_selection_id.replace("3,", ""), park="駐車場あり", rent__gte='5'
                )
            elif '4' in user_list.fab_selection_id:
                user_fab = Article.objects.distinct().filter(
                       address__contains=user_list.fab_selection_id.replace("4,", ""), park="駐車場なし", rent__gte='5'
                )
            fab_selection_list.append(user_fab)
            print(fab_selection_list)
        context["fab_selection_list"] = fab_selection_list

        """
        検索部分
        """

        article = self.request.GET.get('name')
        if article is "" or article is None:
            article = "選択なし"

        address = self.request.GET.get('article_address')
        if address is "" or address is None:
            address = '選択なし'

        floor_list = self.request.GET.getlist('floor')
        if floor_list == []:
            floor = '選択なし'
        else:
            for list_value in floor_list:
                floor = list_value

        room_list = self.request.GET.getlist('room')
        if room_list == []:
            room = '選択なし'
        else:
            for list_value in room_list:
                room = list_value

        live_list = self.request.GET.getlist('live')
        if live_list == [] :
            live = '選択なし'
        else:
            for list_value in live_list:
                live = list_value

        price_list = self.request.GET.getlist('price')
        if price_list == []:
            price = '選択なし'
        else:
            for list_value in price_list:
                price = list_value

        if self.request.user.is_staff is True:
            if article is not None or address is not None or floor is not None or room is not None:
                object_list = object_list.order_by('id', 'article_name', 'address', 'floor_number', 'floor_plan', 'live_flag').filter(
                        Q(article_name__contains=article) | Q(address__contains=address)
                ).filter(customer=self.request.user.id)
                if not object_list:
                    object_list = object_list.order_by('id', 'article_name', 'address', 'floor_number', 'floor_plan', 'live_flag').filter(
                        Q(floor_number__contains=floor) | Q(floor_plan__contains=room)
                    ).filter(customer=self.request.user.id)

                if not object_list:
                    articlelive_list = ArticleLive.objects.all()
                    for check_live in live:
                        if check_live == '0':
                            tmp_live = []
                            articlelive_list = articlelive_list.filter(vacancy_info=check_live)
                            for article_list in articlelive_list:
                                print(article_list)
                                object_list = self.model.objects.all().filter(
                                        customer=self.request.user.id, live_flag=article_list.id
                                )


                        else:
                            articlelive_list = articlelive_list.order_by("id").filter(vacancy_info=check_live)

                            for article_list in articlelive_list:
                                object_list = self.model.objects.all().filter(
                                         customer=self.request.user.id, live_flag=article_list.id
                                )
        else:
            tmp_list = []
            if article is not None or address is not None or floor is not None or room is not None or price is not None or live is not None:
                if live == '選択なし':
                    if price == '選択なし':
                        object_list = Article.objects.distinct().filter(
                                Q(article_name__contains=article) | Q(address__contains=address) |  Q(floor_number__contains=floor) | Q(floor_plan__contains=room)
                        )
                        tmp_list.append(object_list)
                    elif price == '1':
                        object_list = Article.objects.distinct().filter(
                                Q(article_name__contains=article) | Q(address__contains=address) |  Q(floor_number__contains=floor) | Q(floor_plan__contains=room)|
                                Q(rent__lte="3")
                        )
                        tmp_list.append(object_list)
                    elif price == '2':

                        object_list = Article.objects.distinct().filter(
                                Q(article_name__contains=article) | Q(address__contains=address) |  Q(floor_number__contains=floor) | Q(floor_plan__contains=room)|
                                Q(rent__lte= "5") , Q(rent__gte="3")
                        )
                        tmp_list.append(object_list)
                    elif price == '3':
                        object_list = Article.objects.distinct().filter(
                                Q(article_name__contains=article) | Q(address__contains=address) |  Q(floor_number__contains=floor) | Q(floor_plan__contains=room)|
                                Q(rent__lte= "7") , Q(rent__gte="5")
                        )
                        tmp_list.append(object_list)
                    elif price == '4':
                        object_list = Article.objects.distinct().filter(
                                Q(article_name__contains=article) | Q(address__contains=address) |  Q(floor_number__contains=floor) | Q(floor_plan__contains=room)|
                                Q(rent__gte="7")
                        )
                        tmp_list.append(object_list)
                else:
                    articlelive_list = ArticleLive.objects.filter(vacancy_info=live)
                    for article_list in articlelive_list:
                        if price == '選択なし':
                            object_list = Article.objects.all().filter(
                                    Q(live_flag=article_list.id)| Q(article_name__contains=article) | Q(address__contains=address) |  Q(floor_number__contains=floor) | Q(floor_plan__contains=room)
                            ).distinct()
                            print(object_list)
                            tmp_list.append(object_list)

                        elif price == '1':
                            object_list = Article.objects.distinct().filter(
                                    Q(live_flag__exact=article_list.id)| Q(article_name__contains=article) | Q(address__contains=address) |  Q(floor_number__contains=floor) | Q(floor_plan__contains=room)|
                                    Q(rent__lte="3")
                            )
                            tmp_list.append(object_list)
                        elif price == '2':
                            object_list = Article.objects.distinct().filter(
                                    Q(live_flag__exact=article_list.id)| Q(article_name__contains=article) | Q(address__contains=address) |  Q(floor_number__contains=floor) | Q(floor_plan__contains=room)|
                                    Q(rent__lte= "5"), Q(rent__gte="3")
                            )
                            tmp_list.append(object_list)
                        elif price == '3':
                            object_list = Article.objects.distinct().filter(
                                    Q(live_flag__exact=article_list.id)| Q(article_name__contains=article) | Q(address__contains=address) |  Q(floor_number__contains=floor) | Q(floor_plan__contains=room)|
                                    Q(rent__lte= "5"), Q(rent__gte="7")
                            )
                            tmp_list.append(object_list)
                        elif price == '4':
                            object_list = Article.objects.distinct().filter(
                                    Q(live_flag__exact=article_list.id)| Q(article_name__contains=article) | Q(address__contains=address) |  Q(floor_number__contains=floor) | Q(floor_plan__contains=room)|
                                    Q(rent__gte="7")
                            )
                            tmp_list.append(object_list)
            if not tmp_list[0] :
                if self.request.user.is_staff is False:

                    object_list = self.model.objects.all().order_by('id', 'article_name', 'address', 'floor_number', 'floor_plan', "live_flag")
                    tmp_list.append(object_list)
                else:
                    object_list = self.model.objects.all().filter(customer=self.request.user.id).order_by('id', 'article_name', 'address', 'floor_number', 'floor_plan', "live_flag")
                    tmp_list.append(object_list)

            context["tmp_list"] = tmp_list
            return context

    def post(self, request, *args, **kwargs):

        if request.POST.get("fab"):
            print(request.POST.get("fab"))
            fab_db = Fab.objects.filter(user_id=request.user.id, article_id=request.POST.get("fab"))
            is_fab = Fab.objects.filter(user_id=request.user.id, article_id=request.POST.get("fab")).values("flag")
            if not is_fab:
                Fab(user_id=request.user.id, article_id=request.POST.get("fab"), flag=1).save()
            # unlike
            for fab in is_fab:
                if fab['flag']> 0:
                    fab_db.update(flag=0)
                    context = [{
                       'message': 'test'
                    }]
                    return HttpResponse(context)
                # like
                else:
                    fab_db.update(flag=1)
                    context = [{
                       'message': 'test'
                    }]
                    return HttpResponse(context)
"""
詳細情報
"""
class InfoView(generic.ListView):
    model = Article
    template_name = 'apps/info.html'

    def get_context_data(self, **kwargs):

        get = self.request.path.replace('/roomii/info/', '')
        context = super(InfoView, self).get_context_data(**kwargs)
        floor_list = ArticleFloor.objects.all().order_by('floor_id')
        room_list = ArticleRoom.objects.all().order_by('room_id')
        fab_view = Fab.objects.all().filter(user=self.request.user.id).order_by('article_id','flag')
        room_view = RoomImage.objects.all().filter(article_id=get).order_by("id" ,"image")

        context['floor_list'] = floor_list
        context['room_list'] = room_list
        context['fab_view'] = fab_view
        context["room_view"] = room_view

        return context

    def get_queryset(self, **kwargs):
        get = self.request.path.replace('/roomii/info/', '')
        context = super(InfoView, self).get_queryset()
        object_list = self.model.objects.filter(id=get)

        return object_list

"""
物件登録
"""
class ArticleEdit(generic.CreateView):
    model = ArticleCreate
    form_class= Createform
    template_name = 'company/create_form.html'
    success_url = reverse_lazy('apps:top')

    def form_valid(self, form):
        tmp_list = []
        live_id = ArticleLive.objects.order_by('id').reverse()[0]
        user = self.request.user.id
        main_file = form.save(commit=False)
        vacant = self.request.POST["live_flag"]
        info = self.request.POST["info"]
        if info == '':
            info = '貸出可'
        start_date = self.request.POST["start_date"]
        if start_date is None:
            if start_date != "":
                start_date = '選択なし'
        update_date = self.request.POST["update_date"]
        if update_date is None:
            if update_date != "":
                update_date = "選択なし"
        cancel_date = self.request.POST["cancel_date"]
        if cancel_date is None:
            if cancel_date != "":
                cancel_date = "選択なし"

        file_id = Article.objects.order_by('id').reverse()[0]
        count = file_id.id + 1
        vacant_info = ArticleLive.objects.create(article_id=count, vacancy_info=vacant, vacancy_live=info,
                                                 start_date=start_date, update_date=update_date, cancel_date=cancel_date)

        main_file.park = self.request.POST["park"]
        main_file.floor_plan = self.request.POST["floor_plan"]
        main_file.floor_number = self.request.POST["floor_number"]
        main_file.initial_cost = self.request.POST["initial_cost"]
        main_file.common_service_expense = self.request.POST["common_service_expense"]
        main_file.term_of_contract = self.request.POST["term_of_contract"]
        main_file.column = self.request.POST["column"]
        main_file.live_flag_id = vacant_info.id
        main_file.customer = self.request.user.id

        for other_file in main_file.others:
            tmp_list.append(other_file.id)
            other_file.save()
        main_file.room_images_id = tmp_list
        main_file.save()
        vacant_info.save()

        return super(ArticleEdit, self).form_valid(form)

"""
物件編集
"""
class ArticleUpdate(generic.UpdateView):
    model =Article
    form_class = ArticleUpdateForm
    template_name = 'company/update_form.html'
    success_url = reverse_lazy('apps:top')


    def get_context_data(self, **kwargs):
        context = super(ArticleUpdate, self).get_context_data(**kwargs)

        get = self.request.path.replace('/roomii/update/', '')
        list_view = Article.objects.order_by('id').filter(id=get)
        live_list = ArticleLive.objects.order_by('id').filter(article_id=get)

        context["live_list"] = live_list
        context["list_view"] = list_view

        return context

    def post(self, request, **kwargs):

        get_id = self.request.path.replace('/roomii/update/', '')

        tmp_list = []

        vacant = self.request.POST["live_flag"]
        info = self.request.POST["info"]
        if info == '':
            info = '貸出可'
        start_date = self.request.POST["start_date"]
        if start_date is None:
            if start_date != "":
                if info != "":
                    start_date = '選択なし'
                else:
                    start_date = '選択なし'
        update_date = self.request.POST["update_date"]
        if update_date is None:
            if update_date != "":
                if info != "":
                    update_date = "選択なし"
                else:
                    update_date = "選択なし"

        cancel_date = self.request.POST["cancel_date"]
        if cancel_date is None:
            if cancel_date != "":
                if info != "":
                    cancel_date = "選択なし"
                else:
                    cancel_date = "選択なし"

        vacant_info_table = ArticleLive.objects.filter(article_id=get_id)
        for vacant_info in vacant_info_table:
            vacant_info.vacancy_info = vacant
            vacant_info.vacancy_live = info
            vacant_info.start_date = start_date
            vacant_info.update_date = update_date
            vacant_info.cancel_date = cancel_date

        main_table = Article.objects.filter(id=get_id)
        upload_file = self.request.FILES.get('article_image')
        print(upload_file.name)
        for main in main_table:
            main.article_image = upload_file.name
            main.article_name = self.request.POST["article_name"]
            main.comments = self.request.POST["comments"]
            main.address = self.request.POST["address"]
            main.rent = self.request.POST["rent"]
            main.park = self.request.POST["park"]
            main.floor_plan = self.request.POST["floor_plan"]
            main.floor_number = self.request.POST["floor_number"]
            main.initial_cost = self.request.POST["initial_cost"]
            main.common_service_expense = self.request.POST["common_service_expense"]
            main.term_of_contract = self.request.POST["term_of_contract"]
            main.column = self.request.POST["column"]
            main.live_flag_id = vacant_info.id
            main.customer = self.request.user.id

        upload_files = self.request.FILES.getlist('files')
        print(upload_files)
        other_files = []
        for files in upload_files:
            img_filename = Image.open(files)
            img_filename.save(os.path.join('./media/', files.name))
            other_files.append(files.name)

        tmp_room_images_id = []
        for file_image in other_files:
            RoomImage(article_id=self.request.path.replace('/roomii/update/', ''), image=file_image).save()
            tmp_room_images_id.append(RoomImage.id)
        main.room_images_id = str(tmp_room_id)

        img_file = self.request.FILES['article_image'].name
        img_filename = Image.open(self.request.FILES['article_image'])
        img_filename.save(os.path.join('./media/', img_file))

        main.save()
        vacant_info.save()

        return redirect('apps:top')

"""
Googleログイン
"""

class RedirectGoogle(View):

    def get(self, request, *args, **kwargs):
        SCOPE = [
                "https://www.googleapis.com/auth/userinfo.profile",
                "https://www.googleapis.com/auth/userinfo.email"
        ]


        flow = flow_from_clientsecrets(
           './client_id.json',
           scope=SCOPE,
           redirect_uri= "http://localhost:8000/auth/complete/google-oauth2/")

        auth_uri = flow.step1_get_authorize_url()

        return redirect(auth_uri)

class Accesstoken(View):

    def get(self, request, **kwargs):

        if request.GET.get('code'):
            data = google_login_flow(request.GET.get('code'))
            if data['id']:
                check = check_socials(data['id'], 'google')
                if check is not False:
                    social = session.query(UserAuth).join(
                             Social, UserAuth.id == Social.user_id).filter(
                             Social.provider == 'google',
                             Social.provider_id == data['id']).first()
                    if social:
                        check_user = Get_user.objects.filter(username=social.username, password=social.password)
                        for user in check_user:
                            if social.is_active:
                                login(self.request, user)
                                return redirect("apps:top")
                            else:
                                return redirect("apps:login")
                    else:
                        return redirect("apps:login")

                else:
                    user = create_socials_user(data)
                    create_socials(user.id, data, 'google')

                    check_user = Get_user.objects.filter(username=user.username, password=user.password)
                    for user in check_user:
                        if user.is_active:
                            login(self.request, user)
                            return redirect("apps:top")
                        else:
                            return redirect("apps:login")
            else:
                return redirect('apps:login')
        else:
            return redirect('apps:login')

"""
Facebook, ログイン認証
"""
class RedirectFacebook(View):

    def get(self, request, **kwargs):

        url = 'https://www.facebook.com/v3.2/dialog/oauth'
        params = {
            'response_type': 'code',
            'redirect_uri': FACEBOOK_CALLBACK_URL,
            'client_id': SOCIAL_AUTH_FACEBOOK_KEY,
        }

        redirect_url = requests.get(url, params=params).url

        return redirect(redirect_url)

class CallbackFacebook(View):

    def get(self, request, **kwargs):
        if request.GET.get('code'):
            access_token = get_facebook_access_token(request.GET.get('code'))
            data = check_facebook_access_token(access_token)
            if data['is_valid']:
                data = get_facebook_user_info(access_token, data['user_id'])

                social = check_socials(data, 'facebook')
                if social is not False:
                    check_user = Get_user.objects.filter(id=social.user_id)
                    if check_user:
                        for user in check_user:
                            if user.is_active:
                                login(self.request, user)
                                return redirect("apps:top")
                            else:
                                return redirect("apps:login")
                    else:
                        return redirect("apps:login")
                else:
                    user = create_facebook_user(data)
                    social = create_socials(user, data, 'facebook')
                    check_user = Get_user.objects.filter(username=user.username, password=user.password)
                    for user in check_user:
                        if user.is_active:
                            login(self.request, user)
                            return redirect("apps:top")
                        else:
                            return redirect("apps:login")
            else:
                return redirect('apps:login')
