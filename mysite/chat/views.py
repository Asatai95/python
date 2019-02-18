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
        user_id = request.path.split('/').pop(4)
        article_id = request.path.split('/').pop(5)
        message = self.model.objects.filter(message_flag=1, article=article_id, user=user_id) 
        if not message:
            return redirect("register:user_detail", request.user.username, request.user.pk)
        else:
            if not request.user.is_staff:
                article_info = Article.objects.order_by('id').filter(id=article_id)
               
                for info in article_info:
                    company_info_id = info.company_id
                    chat_room = Chat_room.objects.filter(user_id=request.user.id, company_id=company_info_id, article_id=article_id)
                  
                    company_info = Company.objects.order_by('id').filter(id=company_info_id )
                                   
                    return render(request, self.template_name, {'view': company_info, 'chat': chat_room, 'article_id': article_id, 'user_info': user_id, 
                         'user_id': mark_safe(json.dumps(user_id)),
                         'article_id': mark_safe(json.dumps(article_id)) } )
            else:
                company_user_name = request.path.split('/').pop(3)
                article_info = Article.objects.order_by('id').filter(id=article_id)
               
                for info in article_info:
                    company_info_id = info.company_id
                    user_info = Get_user.objects.order_by('id').filter(id=user_id)
                    chat_room = Chat_room.objects.filter(user_id=user_id, company_id=company_info_id, article_id=article_id)
                    user_company = Get_user.objects.filter(username=company_user_name)
                    for user in user_company:
                        company_info = Company.objects.order_by('id').filter(id=company_info_id, user_id=user.id, email=user.email )
                        print(company_info)
                        return render(request, self.template_name, {'view': user_info, 'chat': chat_room, 'company_info': company_info,
                            'user_id': mark_safe(json.dumps(user_id)),
                            'article_id': mark_safe(json.dumps(article_id)) } )


    # def post(self, request, *args, **kwargs):

    #     image = request.FILES["icon"]
    #     print(image)
    #     image = image.name
    #     print(image)

    #     image_table = Chat_room.objects.all()
    #     for table_list in image_table:
    #         table_list.img = image

    #     table_list.save()
    #     print(table_list)