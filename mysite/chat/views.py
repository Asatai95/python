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

#
# from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
# from django.contrib.auth.views import (
#     LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView,
#     PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
# )

from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.utils.translation import gettext_lazy as _
from django.contrib import messages

from django.db import models
from django.db.models import Q
from mysite.models import Article, RoomImage, Fab, ArticleRoom, ArticleFloor, ArticleLive, ArticleCreate, CompanyCreate, Company, License, test_image, Chat_room
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.core.signing import BadSignature, SignatureExpired, loads, dumps
from django.http import Http404, HttpResponseBadRequest
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
#
# from .forms import (
#     LoginForm, UserCreateForm, MyPasswordChangeForm, MyPasswordResetForm, MySetPasswordForm,
#     UserUpdateForm, Createform, LoginCustomerForm, ArticleUpdateForm, CreateCompany, CompanyUpdateForm
# )

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
cloudinary
"""
import cloudinary
import cloudinary.uploader
import cloudinary.api

from django.utils.safestring import mark_safe

import json

class ChatView(View):

    model = Fab
    template_name = 'chat/room.html'

    def get(self, request, *args, **kwargs):
        user_id = request.path.split('/').pop(3)
        aritcle_id = request.path.split('/').pop(4)
        print(aritcle_id)
        message = self.model.objects.filter(message_flag=1, user=user_id, article=aritcle_id) 
        if not message:
            return redirect('register:user_detail')
        else:
            
            article_info = Article.objects.order_by('id').filter(id=aritcle_id)
            for info in article_info:
                company_info_id = info.company_id
                company_info = Company.objects.order_by('id').filter(id=company_info_id)
                chat_room = Chat_room.objects.filter(user_id=user_id, company_id=company_info_id)

            return render(request, self.template_name, {'view': company_info, 'chat': chat_room, 'user_id': user_id, 'aritcle_id':aritcle_id })
    

    # def post(self, request, *args, **kwargs):
    #     user_id = request.user.id
    #     user_name = request.user.username
    #     aritcle_id = request.path.split('/').pop(4)
    #     article_info = Article.objects.order_by('id').filter(id=aritcle_id)
    #     for article in article_info:
    #         company_info = Company.objects.filter(id=article.company_id)
    #         for info in company_info:
