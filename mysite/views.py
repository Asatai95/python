import os
import sys
from PIL import Image
from django import *
from django.conf import settings
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
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
from mysite.models import Article, RoomImage, Fab, ArticleRoom, ArticleFloor, ArticleLive, Imagetest, ArticleCreate
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

"""
Settingファイル
"""
from config.settings import *

"""
データベース
"""
Get_user = get_user_model()
ArticleMain = Article.objects.all()
ArticleImage = RoomImage.objects.all()

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

#
# """
# ログイン機能（業者）
# """
# class LoginCustomer(LoginView):
#
#     form_class= LoginCustomerForm
#     template_name = 'company/login_form.html'
#     success_url = reverse_lazy('apps:customer_top')
#
#     def login_user(request):
#         if request.method == 'POST':
#             email = request.POST['username']
#             user = Get_user.objects.filter(email=email)
#             print(user)
#             password = request.POST['password']
#             print(password)
#             user = authenticate(request, username=user.username, password=password)
#             if user is not None:
#                 django_login(request, user)
#                 return django.http.HttpResponseRedirect('/customer/roomii/')
#

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
TOPページ, 検索機能
"""
class MainView(generic.ListView):
    model = Article
    template_name = 'apps/index.html'

    def get_context_data(self, **kwargs):

        context = super(MainView, self).get_context_data(**kwargs)
        floor_list = ArticleFloor.objects.all().order_by('floor_id')
        room_list = ArticleRoom.objects.all().order_by('room_id', 'room_live_id')
        fab_view = Fab.objects.all().filter(user=self.request.user.id).order_by('article_id','flag')
        live = ArticleLive.objects.all()

        context['floor_list'] = floor_list
        context['room_list'] = room_list
        context['fab_view'] = fab_view
        context['live'] = live

        return context

    def get_queryset(self):

        if self.request.user.is_staff is False:
            object_list = self.model.objects.all().order_by('id', 'article_name', 'address', 'floor_number', 'floor_plan', 'live_flag')
        else:
            object_list = self.model.objects.all().filter(customer=self.request.user.id).order_by('id', 'article_name', 'address', 'floor_number', 'floor_plan', 'live_flag')
        article = self.request.GET.get('name')
        if article is "" or article is None:
            article = "選択なし"
        address = self.request.GET.get('article_address')
        if address is "" or address is None:
            address = '選択なし'
        floor = self.request.GET.getlist('floor')
        if floor is None:
            floor = '選択なし'
        room = self.request.GET.getlist('room')
        if room is None:
            room = '選択なし'
        live = self.request.GET.getlist('live')
        if live is None:
            live = '選択なし'

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
                                object_list |= self.model.objects.all().filter(
                                        customer=self.request.user.id, live_flag=article_list.id
                                )


                        else:
                            articlelive_list = articlelive_list.order_by("id").filter(vacancy_info=check_live)

                            for article_list in articlelive_list:
                                object_list |= self.model.objects.all().filter(
                                         customer=self.request.user.id, live_flag=article_list.id
                                )
        else:
            if article is not None or address is not None or floor is not None or room is not None:
                object_list = self.model.objects.all().filter(
                       Q(article_name__contains=article) | Q(address__contains=address)
                )
                if not object_list:
                    object_list = object_list.filter(
                       Q(floor_number__contains=floor) | Q(floor_plan__contains=room)
                    )

                if not object_list:
                    articlelive_list = ArticleLive.objects.all()
                    for check_live in live:
                        if check_live == '0':
                            tmp_live = []
                            articlelive_list = articlelive_list.filter(vacancy_info=check_live)
                            for article_list in articlelive_list:
                                print(article_list)
                                object_list |= self.model.objects.all().filter(
                                        live_flag=article_list.id
                                )


                        else:
                            articlelive_list = articlelive_list.order_by("id").filter(vacancy_info=check_live)

                            for article_list in articlelive_list:
                                object_list |= self.model.objects.all().filter(
                                         live_flag=article_list.id
                                )
        if self.request.user.is_staff is False:
            if not object_list:
                object_list = self.model.objects.all().order_by('id', 'article_name', 'address', 'floor_number', 'floor_plan', "live_flag")

            return object_list
        else:
            if not object_list:
                object_list = self.model.objects.all().filter(customer=self.request.user.id).order_by('id', 'article_name', 'address', 'floor_number', 'floor_plan', "live_flag")

            return object_list


"""
お気に入り機能
"""
class Like(generic.View):
    def get(request, *args, **kwargs):
        fab_db = Fab.objects.filter(user_id=kwargs['pk'], article_id=kwargs['article_id'])
        is_fab = Fab.objects.filter(user_id=kwargs['pk'], article_id=kwargs['article_id']).values("flag")
        print(is_fab)
        if not is_fab:
            Fab(user_id=kwargs['pk'], article_id=kwargs['article_id'], flag=1).save()
            return redirect("apps:top")
        # unlike
        for fab in is_fab:
            if fab['flag']> 0:
                fab_db.update(flag=0)
                return redirect("apps:top")
            # like
            else:
                fab_db.update(flag=1)
                return redirect("apps:top")

"""
詳細情報
"""
class InfoView(generic.ListView):
    model = Article
    template_name = 'apps/info.html'

    def get_context_data(self, **kwargs):

        context = super(InfoView, self).get_context_data(**kwargs)
        floor_list = ArticleFloor.objects.all().order_by('floor_id')
        room_list = ArticleRoom.objects.all().order_by('room_id')
        fab_view = Fab.objects.all().filter(user=self.request.user.id).order_by('article_id','flag')

        context['floor_list'] = floor_list
        context['room_list'] = room_list
        context['fab_view'] = fab_view

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
    success_url = reverse_lazy('apps:create')

    def form_valid(self, form):
        tmp_list = []
        live_id = ArticleLive.objects.order_by('id').reverse()[0]
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
        count = file_id + 1
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
            file_image = other_file.image
            tmp_list.append(file_image.name)
            other_file.save()
        main_file.room_images_id = str(tmp_list)
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

        for file_image in other_files:
            RoomImage(article_id=self.request.path.replace('/roomii/update/', ''), image=file_image).save()

        main.room_images_id = str(other_files)

        img_file = self.request.FILES['article_image'].name
        img_filename = Image.open(self.request.FILES['article_image'])
        img_filename.save(os.path.join('./media/', img_file))

        main.save()
        vacant_info.save()

        return redirect('apps:top')

"""
test
"""
class Test(generic.View):
    template_name = 'company/test.html'

    def get(self, request, **kwargs):

        return render(request, self.template_name)

    def post(self, request, **kwargs):

        test = request.POST["date"]
        print(test)

        return render(request, self.template_name)
