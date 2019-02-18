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
        self.user_auth = self.scope['url_route']['kwargs']['username']

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
                    self.company_user_auth = await self.get_user_company_info(self.user_auth, company_detail.user_id)
                    if not self.company_user_auth:
                        
                        self.company_id_info = info.company_id
                        self.company_name_info = company_detail.company_name
                        self.user = user_detail.username                       
                    else:
                        
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
        print(message)
        
        await self.channel_layer.group_send (
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
            }
        )

    # async def receive(self, text_data=None, bytes_data=None):
    #     text_data_json = json.loads(text_data)
    #     image = text_data_json["image"]
    #     print(image)
        
    #     await self.channel_layer.group_send (
    #         self.room_group_name,
    #         {
    #             'type': 'chat_image',
    #             "image": image
    #         }
    #     )
        
    async def chat_message(self, event):
       
        message = event['message']
        if message != "":
            await self._save_message(message)
        await self.send(text_data=json.dumps({
            'message': message,
        }))

    # async def chat_image(self, event):
        
    #     image = event["image"]
    #     print(image)

    #     await self.send(text_data=json.dumps({
    #         "image": image
    #     }))

    @database_sync_to_async
    def _save_message(self , message):
        if self.company_user_auth:
            Chat_room.objects.create(
               company_id = self.company_id_info,
               user_id = self.user_info,
               article_id = self.article_info,
               chat= message,
               to_person = self.user,
               from_person = self.company_name_info,
            )
        else:
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
    def get_user_company_info(self, user_name_info, company_user_id):
        user_company = Get_user.objects.filter(id=company_user_id, username=user_name_info, is_staff=1, is_company=1)
        if user_company:
            return True
        else:
            return False

    @database_sync_to_async
    def get_user_info(self, user_id_info):
        user = Get_user.objects.filter(id=user_id_info)
        return user
       