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
from django.core.validators import URLValidator
from django.utils.translation import gettext_lazy as _
from django.contrib import messages

from django.db import models
from django.db.models import Q
from mysite.models import Article, RoomImage, Fab, ArticleRoom, ArticleFloor, ArticleLive, ArticleCreate, CompanyCreate, Company, License, test_image
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.core.signing import BadSignature, SignatureExpired, loads, dumps
from django.http import Http404, HttpResponseBadRequest
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST

from .forms import (
    LoginForm, UserCreateForm, MyPasswordChangeForm, MyPasswordResetForm, MySetPasswordForm,
    UserUpdateForm, Createform, LoginCustomerForm, ArticleUpdateForm, CreateCompany, CompanyUpdateForm
)

import requests

import re

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from pure_pagination.mixins import PaginationMixin

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
cloudinary
"""
import cloudinary
import cloudinary.uploader
import cloudinary.api

"""
画像ファイル制限
"""
MAX_MEMORY_SIZE = 10485760

"""
ページネーション
"""
def paginate_queryset(request, queryset, count):

    paginator = Paginator(queryset, count)
    page = request.GET.get('page')
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return page_obj


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

"""
業者、ユーザー識別
"""
def user_check(user):
    return user.is_staff

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
        return redirect("register:user_create_done")

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

    def get(self, request, **kwargs):

        user_id = request.path.split('/').pop(3)
        print(user_id)
        if not request.user.is_staff:
            tmp_fab = []
            tmp_article = []
            fab = Fab.objects.filter(user=request.user ,message_flag=1, flag=1).values('article', 'updated_at')
            for tmp in fab:
                fab_dic = {'article': tmp['article'], 'updated': tmp['updated_at']}
                tmp_fab.append(fab_dic)

            article = ArticleMain.values('id', 'article_name', 'article_image', 'comments')
            for tmp in article:
                article_dic = {'id': tmp['id'], 'name': tmp['article_name'] ,'image': tmp['article_image'], 'comment': tmp['comments']}
                tmp_article.append(article_dic)

            return render(request, self.template_name, {'fab': tmp_fab, 'list': tmp_article,  })

        else:
            tmp_article_live = []
            tmp_article = []
            tmp_user = []
            tmp_fab = []
            article = Article.objects.filter(customer=request.user.id).order_by("live_flag_id")
            company = CompanyCreate.objects.filter(user_id=request.user.id)
            for main in article:
                tmp_article.append(main)
                articleLive = ArticleLive.objects.filter(id=main.live_flag_id).order_by("vacancy_info")
                for live in articleLive:
                    tmp_article_live.append(live)
                    fab_user_list = Fab.objects.order_by("id").filter(article_id=main.id)
                    tmp_fab.append(fab_user_list)
                    for user_list in fab_user_list:
                        user_info = Get_user.objects.filter(id=user_list.user_id)
                        tmp_user.append(user_info)
                        
            return render(request, self.template_name, {'tmp_article': tmp_article, 'tmp_article_live': tmp_article_live, 'company': company, 'tmp_fab':tmp_fab ,'tmp_user': tmp_user, })

"""
マイページ更新
"""
class UserUpdate(PermissionsMypage, generic.UpdateView):
    model = Get_user
    form_class = UserUpdateForm
    template_name = 'register/user_form.html'

    def form_valid(self, form):

        """
        画像サイズ制限
        """
        img_file_size = self.request.FILES['img_file']
        if img_file_size.size > MAX_MEMORY_SIZE:
            return render(self.request, self.template_name, {'error': "画像容量が超えております。"})
        else:
            return super(UserUpdate, self).form_valid(form)

    def get_success_url(self):

        User = Get_user.objects.all().filter(pk=self.kwargs['pk'])

        try:
            img_file = self.request.FILES['img_file'].name
            img_filename = Image.open(self.request.FILES['img_file'])
            img_filename.save(os.path.join('./static/img/', img_file))
            img_file = os.path.join('/static/img/', img_file)
            for user in User:
                user.image = user
            user.image = img_file
            user.save()

            return resolve_url('register:user_detail', username=self.request.user.username, pk=self.kwargs['pk'])
        except:
            img_file = self.request.POST.get("user_img")
            for user in User:
                user.image = user
            user.image = img_file
            user.save()

            return resolve_url('register:user_detail', username=self.request.user.username, pk=self.kwargs['pk'])

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

        return render(request, self.template_name)

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

class TopSearch(generic.ListView):
    
    model = Article
    template_name = "apps/top.html"

    def get(self, request, *args, **kwargs):

        return render(request, self.template_name)

"""
TOPページ, 検索機能
"""
class MainView(PaginationMixin, generic.ListView):
    model = Article
    template_name = 'apps/index.html'
    paginate_by = 3
    success_url = 'apps:top'

    def get_context_data(self, **kwargs):

        """
        トップ画面表示(一部)
        """
        auth_user_id = self.request.user.id

        context = super(MainView, self).get_context_data(**kwargs)
        user = User.objects.all().filter(id=self.request.user.id).order_by("fab_selection_id")
        floor_table = ArticleFloor.objects.all().order_by('floor_id')
        room_table = ArticleRoom.objects.all().order_by('room_id', 'room_live_id')
        fab_view = Fab.objects.all()
        fab_not_view = Fab.objects.all().filter(user_id=auth_user_id)
        live_table = ArticleLive.objects.all()

        user_auth = self.request.user
        if user_auth.is_staff:
            auth_user = 'c'
        else:
            auth_user = 'u'

        tmp_count = []
        company_info = Company.objects.filter(user_id=auth_user_id)
        for info in company_info:
            article_info = Article.objects.filter(company_id=info.id)
            for info in article_info:
                tmp_count.append(info.article_name)
                count_article = len(tmp_count)
                if int(count_article) > 9:
                    count_over = False
                else:
                    count_over = True
        
        """
        現在の日付取得、最新の記事情報を開示する
        """
        import datetime

        dt = datetime.datetime.utcnow()
        month_first = dt.date() - datetime.timedelta(days=dt.day - 1)
        today = datetime.date.today()
        fab_article = Article.objects.all().filter(created_at__range=(month_first, today))

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
                articlelive_list = ArticleLive.objects.filter(vacancy_info=live)
                for article_list in articlelive_list:
                    live = article_list

        price_list = self.request.GET.getlist('price')
        if price_list == []:
            price = '選択なし'
        else:
            for list_value in price_list:
                price = list_value

        if self.request.user.is_staff is True:
            tmp_list = []
            if article is not None or address is not None or floor is not None or room is not None or price is not None or live is not None:
                if live == '選択なし':
                    if price == '選択なし':
                        object_list = Article.objects.filter(
                                Q(article_name__contains=article) | Q(address__contains=address) |  Q(floor_number__contains=floor) | Q(floor_plan__contains=room)
                        ).filter(customer=self.request.user.id)
                        tmp_list.append(object_list)
                    elif price == '1':
                        object_list = Article.objects.filter(
                                Q(article_name__contains=article) | Q(address__contains=address) |  Q(floor_number__contains=floor) | Q(floor_plan__contains=room)|
                                Q(rent__lte="3")
                        ).filter(customer=self.request.user.id)
                        tmp_list.append(object_list)
                    elif price == '2':

                        object_list = Article.objects.filter(
                                Q(article_name__contains=article) | Q(address__contains=address) |  Q(floor_number__contains=floor) | Q(floor_plan__contains=room)|
                                Q(rent__lte= "5") , Q(rent__gte="3")
                        ).filter(customer=self.request.user.id)
                        tmp_list.append(object_list)
                    elif price == '3':
                        object_list = Article.objects.filter(
                                Q(article_name__contains=article) | Q(address__contains=address) |  Q(floor_number__contains=floor) | Q(floor_plan__contains=room)|
                                Q(rent__lte= "7") , Q(rent__gte="5")
                        ).filter(customer=self.request.user.id)
                        tmp_list.append(object_list)
                    elif price == '4':
                        object_list = Article.objects.filter(
                                Q(article_name__contains=article) | Q(address__contains=address) |  Q(floor_number__contains=floor) | Q(floor_plan__contains=room)|
                                Q(rent__gte="7")
                        ).filter(customer=self.request.user.id)
                        tmp_list.append(object_list)
                else:
                    if price == '選択なし':
                        object_list = Article.objects.filter(
                                Q(live_flag=article_list.id)| Q(article_name__contains=article) | Q(address__contains=address) |  Q(floor_number__contains=floor) | Q(floor_plan__contains=room)
                        ).filter(customer=self.request.user.id)
                        tmp_list.append(object_list)

                    elif price == '1':
                        object_list = Article.objects.filter(
                                Q(live_flag__exact=article_list.id)| Q(article_name__contains=article) | Q(address__contains=address) |  Q(floor_number__contains=floor) | Q(floor_plan__contains=room)|
                                Q(rent__lte="3")
                        ).filter(customer=self.request.user.id)
                        tmp_list.append(object_list)
                    elif price == '2':
                        object_list = Article.objects.filter(
                                Q(live_flag__exact=article_list.id)| Q(article_name__contains=article) | Q(address__contains=address) |  Q(floor_number__contains=floor) | Q(floor_plan__contains=room)|
                                Q(rent__lte= "5"), Q(rent__gte="3")
                        ).filter(customer=self.request.user.id)
                        tmp_list.append(object_list)
                    elif price == '3':
                        object_list = Article.objects.filter(
                                Q(live_flag__exact=article_list.id)| Q(article_name__contains=article) | Q(address__contains=address) |  Q(floor_number__contains=floor) | Q(floor_plan__contains=room)|
                                Q(rent__lte= "5"), Q(rent__gte="7")
                        ).filter(customer=self.request.user.id)
                        tmp_list.append(object_list)
                    elif price == '4':
                        object_list = Article.objects.filter(
                                Q(live_flag__exact=article_list.id)| Q(article_name__contains=article) | Q(address__contains=address) |  Q(floor_number__contains=floor) | Q(floor_plan__contains=room)|
                                Q(rent__gte="7")
                        ).filter(customer=self.request.user.id)
                        tmp_list.append(object_list)
        else:
            tmp_list = []
            if article is not None or address is not None or floor is not None or room is not None or price is not None or live is not None:
                if live == '選択なし':
                    if price == '選択なし':
                        object_list = Article.objects.filter(
                                Q(article_name__contains=article) | Q(address__contains=address) |  Q(floor_number__contains=floor) | Q(floor_plan__contains=room)
                        )
                        tmp_list.append(object_list)
                    elif price == '1':
                        object_list = Article.objects.filter(
                                Q(article_name__contains=article) | Q(address__contains=address) |  Q(floor_number__contains=floor) | Q(floor_plan__contains=room)|
                                Q(rent__lte="3")
                        )
                        tmp_list.append(object_list)
                    elif price == '2':

                        object_list = Article.objects.filter(
                                Q(article_name__contains=article) | Q(address__contains=address) |  Q(floor_number__contains=floor) | Q(floor_plan__contains=room)|
                                Q(rent__lte= "5") , Q(rent__gte="3")
                        )
                        tmp_list.append(object_list)
                    elif price == '3':
                        object_list = Article.objects.filter(
                                Q(article_name__contains=article) | Q(address__contains=address) |  Q(floor_number__contains=floor) | Q(floor_plan__contains=room)|
                                Q(rent__lte= "7") , Q(rent__gte="5")
                        )
                        tmp_list.append(object_list)
                    elif price == '4':
                        object_list = Article.objects.filter(
                                Q(article_name__contains=article) | Q(address__contains=address) |  Q(floor_number__contains=floor) | Q(floor_plan__contains=room)|
                                Q(rent__gte="7")
                        )
                        tmp_list.append(object_list)
                else:
                    if price == '選択なし':
                        object_list = Article.objects.filter(
                                Q(live_flag=article_list.id)| Q(article_name__contains=article) | Q(address__contains=address) |  Q(floor_number__contains=floor) | Q(floor_plan__contains=room)
                        )
                        print(object_list)
                        tmp_list.append(object_list)

                    elif price == '1':
                        object_list = Article.objects.filter(
                                Q(live_flag__exact=article_list.id)| Q(article_name__contains=article) | Q(address__contains=address) |  Q(floor_number__contains=floor) | Q(floor_plan__contains=room)|
                                Q(rent__lte="3")
                        )
                        print(object_list)
                        tmp_list.append(object_list)
                    elif price == '2':
                        object_list = Article.objects.filter(
                                Q(live_flag__exact=article_list.id)| Q(article_name__contains=article) | Q(address__contains=address) |  Q(floor_number__contains=floor) | Q(floor_plan__contains=room)|
                                Q(rent__lte= "5"), Q(rent__gte="3")
                        )
                        tmp_list.append(object_list)
                    elif price == '3':
                        object_list = Article.objects.filter(
                                Q(live_flag__exact=article_list.id)| Q(article_name__contains=article) | Q(address__contains=address) |  Q(floor_number__contains=floor) | Q(floor_plan__contains=room)|
                                Q(rent__lte= "5"), Q(rent__gte="7")
                        )
                        tmp_list.append(object_list)
                    elif price == '4':
                        object_list = Article.objects.filter(
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
        
        page_obj = paginate_queryset(self.request, object_list, 10)
      
        return super(MainView, self).get_context_data(
                tmp_list=tmp_list, page_obj=page_obj, fab_selection_list=fab_selection_list, fab_not_view=fab_not_view, live_table=live_table, floor_table=floor_table, 
                room_table=room_table, floor_list=floor_list, room_list=room_list, fab_view=fab_view, live=live, fab_article=fab_article, auth_user=auth_user, count_over=count_over, **kwargs
            )
            
    def render_to_response(self, context, **response_kwargs):
        # if not self.request.GET.get:
        #    return redirect("apps:top_search")

        return super(MainView, self).render_to_response(
               context, **response_kwargs
           )

    def post(self, request, *args, **kwargs):

        if request.POST.get("fab"):
            if request.user.id:
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
            else:
                return False
        
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
業者登録
"""

class CompanyView(generic.CreateView):
    model = CompanyCreate
    form_class = CreateCompany
    template_name = "company/company.html"
    success_url = reverse_lazy("apps:create")

    def get(self, request, *args, **kwargs):

        if not request.user.is_staff:
            return redirect("apps:top")

        if CompanyCreate.objects.filter(user_id=request.user.id, is_company=1):
            return redirect("apps:create")

        tmp_count = []
        company_info = Company.objects.filter(user_id=self.request.user.id)
        for info in company_info:
            article_info = Article.objects.filter(company_id=info.id)
            for info in article_info:
                tmp_count.append(info.article_name)
                count_article = len(tmp_count)
                if int(count_article) > 9:
                    count_over = False
                else:
                    count_over = True

        form = self.form_class()
        return render(request, self.template_name, {'form':form, 'count_over': count_over})

    def form_valid(self, form):

        company = form.save(commit=False)

        """
        画像サイズ制限
        """
        img_file_size = self.request.FILES['company_image']
        if img_file_size.size > MAX_MEMORY_SIZE:
            return render(self.request, self.template_name, {'error': "画像容量が超えております。"})

        address_number = self.request.POST.get("address_number")
        address = self.request.POST.get("address")
        address_city = self.request.POST.get("address_city")
        address_others = self.request.POST.get("address_others")
        user_table = Get_user.objects.filter(id=int(self.request.user.id))
        for user_is_company in user_table:
            user_is_company.is_company = 1
        img_file = self.request.FILES['company_image'].name
        img_filename = Image.open(self.request.FILES['company_image'])
        img_filename.save(os.path.join('./static/img/', img_file))

        if company:
            company.is_company = 1
            company.user_id = int(self.request.user.id)
            company.update_count = self.request.POST.get("update_count")
            company.address_number = address_number
            company.address = address + ' ' + address_city + ' ' + address_others
            company.license = self.request.POST.get("license")
        company.save()
        user_is_company.save()
        if form:
            return super(CompanyView, self).form_valid(form)
        else:
            return redirect("apps:company")

"""
業者編集
"""
class CompanyChange(generic.UpdateView):
    model = Company
    form_class = CompanyUpdateForm
    template_name = 'company/company_update.html'
    success_url = reverse_lazy('apps:user_detail')

    def get(self, request, *args, **kwargs):
        user = request.user.id
        tmp_count = []
        company_info = Company.objects.filter(user_id=self.request.user.id)
        for info in company_info:
            article_info = Article.objects.filter(company_id=info.id)
            for info in article_info:
                tmp_count.append(info.article_name)
                count_article = len(tmp_count)
                if int(count_article) > 9:
                    count_over = False
                else:
                    count_over = True

        company = Company.objects.filter(user_id=user)
        if not request.user.is_staff:
            return redirect('apps:top')
        return render(request, self.template_name, {'company': company, 'count_over': count_over})

    def post(self, request, *args, **kwargs):

        company = Company.objects.filter(user_id=request.user.id)
        company_name = request.POST.get("company_name")
        address_number = request.POST.get("address_number")
        print(address_number)
        address = request.POST.get("address")

        email = request.POST.get('email')
        email_pattern = r"[^@]+@[^@]+\.[^@]+"
        email_match = re.match(email_pattern, email)

        license_year = request.POST.get("license_year")
        if license_year == '':
            for license in company:
                license_year = license.update_count

        tel = request.POST.get("tel_number")
        pattern = r"[\(]{0,1}[0-9]{2,4}[\)\-\(]{0,1}[0-9]{2,4}[\)\-]{0,1}[0-9]{3,4}"
        tel_number = re.match(pattern, tel)

        license_number = request.POST.get("license")
        license = license_number.replace("第", "").replace("号", "")
        check = re.match(r'^[0-9]+$', license)

        if check is None or tel_number is None or email_match is None:
            context = {
                 'error_tel': '正しい番号を入力してください',
                 'error_license': '数字は半角英数字で入力してください',
                 "error_email": "正しいEmailを入力してください",
                 'company': company
            }
            return render(request, self.template_name, context)

        url = request.POST.get("web")
        if 'http://' not in url :
            if 'https://' not in url:
                context = {
                     'error_url': '正しいURLを入力してください',
                     'company': company
                }
                return render(request, self.template_name, context)
            else:
                pass
        else:
            pass
        """
        画像サイズ制限
        """
        img_file_size = self.request.FILES['company_image']
        if img_file_size.size > MAX_MEMORY_SIZE:
            return render(self.request, self.template_name, {'error': "画像容量が超えております。"})

        company_table = Company.objects.filter(user_id=request.user.id)
        try:
            upload_file = request.FILES.get('company_image')
            img_filename = Image.open(upload_file)
            img_filename.save(os.path.join('./media/', upload_file.name))
        except:
            upload_file = request.POST.get("company_image_hidden")

        for company_info in company_table:
            company_info.company_name= company_name
            company_info.address_number = address_number
            company_info.address = address
            company_info.update_count = license_year
            company_info.license = license_number
            company_info.email = email
            company_info.web = url
            company_info.tel_number = tel
            try:
                company_info.company_image = upload_file.name
            except:
                company_info.company_image = upload_file

        company_info.save()

        return redirect('apps:top')

"""
物件登録
"""
class ArticleEdit(generic.CreateView):
    model = ArticleCreate
    form_class= Createform
    template_name = 'company/create_form.html'
    success_url = reverse_lazy('apps:top')

    def get(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect('apps:top')

        tmp_count = []
        company_info = Company.objects.filter(user_id=self.request.user.id)
        for info in company_info:
            article_info = Article.objects.filter(company_id=info.id)
            for info in article_info:
                tmp_count.append(info.article_name)
                count_article = len(tmp_count)
                if int(count_article) > 9:
                    count_over = False
                else:
                    count_over = True

        form = self.form_class()
        return render(request, self.template_name, {'form': form, 'count_over': count_over})

    def form_valid(self, form):

        """
        画像サイズ制限
        """
        upload_files = self.request.FILES.getlist("files")
        for img_file_size in upload_files:
            if img_file_size.size > MAX_MEMORY_SIZE:    
                return render(self.request, self.template_name, {'error': "画像容量が超えております。"})
        
        tmp_list = []
        company_id = Company.objects.filter(user_id=self.request.user.id)
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
        address_town = self.request.POST["address"]
        address_city = self.request.POST["address_city"]
        address_others = self.request.POST["address_others"]
        for company in company_id:
            main_file.company_id = company.id
        main_file.address_number = self.request.POST["address_number"]
        main_file.address = address_town + ' ' + address_city + ' ' + address_others
        main_file.rent = self.request.POST["rent"]
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

        tmp_count = []
        company_info = Company.objects.filter(user_id=self.request.user.id)
        for info in company_info:
            article_info = Article.objects.filter(company_id=info.id)
            for info in article_info:
                tmp_count.append(info.article_name)
                count_article = len(tmp_count)
                if int(count_article) > 9:
                    count_over = False
                else:
                    count_over = True

        return super(ArticleUpdate, self).get_context_data(
                live_list=live_list, list_view=list_view, count_over=count_over, **kwargs
            )

    def render_to_response(self, context, **response_kwargs):
       if not self.request.user.is_staff:
           return redirect("apps:top")
       get = self.request.path.replace('/roomii/update/', '')
       article_check = Article.objects.order_by('id').filter(id=get, customer=self.request.user.id)
       if article_check:
           return super(ArticleUpdate, self).render_to_response(
               context, **response_kwargs
           )
       else:
           return redirect('apps:top')

    def post(self, request, **kwargs):

        get_id = self.request.path.replace('/roomii/update/', '')
        article = self.model.objects.filter(id=get_id)
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

        try:
            upload_file = self.request.FILES.get('article_image')
            img_filename = Image.open(upload_file)
            img_filename.save(os.path.join('./media/', upload_file.name))
        except:
            upload_file = self.request.POST.get("article_image_hidden")

        for main in main_table:
            try:
                main.article_image = upload_file.name
            except:
                main.article_image = upload_file
            main.article_name = self.request.POST["article_name"]
            main.comments = self.request.POST["comments"]
            main.address_number = self.request.POST["address_number"]
            main.address = self.request.POST["address"]
            main.rent = self.request.POST["rent"]
            try:
                main.park = self.request.POST["park"]
            except:
                for article_park in article:
                    main.park = article_park.park
            try:
                main.floor_plan = self.request.POST["floor_plan"]
            except:
                for article_floor_plan in article:
                    main.floor_plan = article_floor_plan.floor_plan
            try:
                main.floor_number = self.request.POST["floor_number"]
            except:
                for article_floor_number in article:
                    main.floor_number = article_floor_number.floor_number
            main.initial_cost = self.request.POST["initial_cost"]
            main.common_service_expense = self.request.POST["common_service_expense"]
            main.term_of_contract = self.request.POST["term_of_contract"]
            main.column = self.request.POST["column"]
            main.live_flag_id = vacant_info.id
            main.customer = self.request.user.id
        
        """
        画像サイズ制限
        """
        upload_files = self.request.FILES.getlist('files')
        for img_file_size in upload_files:
            if img_file_size.size > MAX_MEMORY_SIZE:
                return render(self.request, self.template_name, {'error': "画像容量が超えております。"})
                
        other_files = []
        try:
            for files in upload_files:
                img_filename = Image.open(files)
                img_filename.save(os.path.join('./media/', files.name))
                other_files.append(files.name)

            tmp_room_images_id = []
            for file_image in other_files:
                RoomImage(article_id=self.request.path.replace('/roomii/update/', ''), image=file_image).save()
                tmp_room_images_id.append(RoomImage.id)
            main.room_images_id = str(tmp_room_id)

            """
            画像ファイル制限
            """
            img_file_size = self.request.FILES['article_image']
            if img_file_size.size > MAX_MEMORY_SIZE:
                return render(self.request, self.template_name, {'error': "画像容量が超えております。"})

            img_file = self.request.FILES['article_image'].name
            img_filename = Image.open(self.request.FILES['article_image'])
            img_filename.save(os.path.join('./media/', img_file))
        except:
            main.room_images_id = self.request.POST.get("files_hidden")

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
                                return redirect("apps:login_after")
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
                            return redirect("apps:login_after")
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

        url = 'http://www.facebook.com/v3.2/dialog/oauth'
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
                                return redirect("apps:login_after")
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
                            login(request, user)
                            return redirect("apps:login_after")
                        else:
                            return redirect("apps:login")
            else:
                return redirect('apps:login')


class image(View):

    model = test_image
    template_name = 'apps/test_image.html'

    def upload(file, **options):
        table = self.model.objects.all()
        for table_list in table:
            cloudinary.uploader.upload(table_list.image)

    def get(self, request, *args, **kwargs):

        table = self.model.objects.all()
        for table_list in table:
            context = {
                 'test': table_list
            }
        return render(request, self.template_name, context)
