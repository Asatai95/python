from django import *
from mysite.routing import * 
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from mysite.models import Article, Fab, ArticleLive, Chat_room, Company, Test
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync
from channels.auth import login
import asyncio
from django.contrib.auth import get_user_model, authenticate

import json

from django.conf import settings
from django.db import models


import requests

import re

"""
Settingファイル
"""
from config.settings import *


"""
ユーザーモデル
"""
Get_user = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    
    model = Chat_room

    async def connect(self):
        self.article_info = self.scope['url_route']['kwargs']['article_id']
        self.user_info = self.scope['url_route']['kwargs']['pk']
       
        self.room_group_name = 'chat_%s' % self.article_info
        
        await self.channel_layer.group_add (
            self.room_group_name,
            self.channel_name
        )

        self.article_table_info = await self.get_article_info(self.article_info)
        for info in self.article_table_info:
            self.company_info = await self.get_company_info(info.company_id)
            for company_detail in self.company_info:
                self.user = await self.get_user_info(self.user_info)
                for user_detail in self.user:
                    if not user_detail.is_staff:
                        self.company_id_info = info.company_id
                        self.company_name_info = company_detail.company_name
                        self.user = user_detail.username
                    else:
                        # self.get_company_user = await self.get_company_user_info(info.company_id, self.user_info)
                        # for get_user_info in self.get_company_user:
                            
                        self.company_id_info = info.company_id
                        self.company_name_info = company_detail.company_name
                        self.user = user_detail.username

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard (
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.channel_layer.group_send (
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )
   
    async def chat_message(self, event):
        
        message = event['message']
        if message != "":
            await self._save_message(message)
        await self.send(text_data=json.dumps({
            'message': message
        }))

    @database_sync_to_async
    def _save_message(self , message):
        Chat_room.objects.create(
            company_id = self.company_id_info,
            user_id = self.user_info,
            article_id = self.article_info,
            chat= message,
            to_person = self.company_name_info,
            from_person = self.user,
        )

    @database_sync_to_async
    def get_article_info(self, id_info):
        article_id_info = Article.objects.filter(id=id_info)
        
        return article_id_info

    @database_sync_to_async
    def get_company_info(self, company_info):
        company = Company.objects.filter(id=company_info)
        return company
    
    @database_sync_to_async
    def get_company_user_info(self, company_info, company_user_id_info):
        company_user = Company.objects.filter(id=company_info, user_id=company_user_id_info)
        return company_user

    @database_sync_to_async
    def get_user_info(selfm, user_id_info):
        user = Get_user.objects.filter(id=user_id_info)
        return user
       