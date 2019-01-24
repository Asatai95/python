from channels.generic.websocket import AsyncWebsocketConsumer
from mysite.models import Article, Fab, ArticleLive, Chat_room
from channels.db import database_sync_to_async
import json


class ChatConsumer(AsyncWebsocketConsumer):
    model = Chat_room
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['user_id']['article_id']
        self.room_group_name = 'chat_%s' % self.room_name
        
        await self.channel_layer.group_add (
            self.room_group_name,
            self.channel_name
        )

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
            self._save_message(message)
        await self.send(text_data=json.dumps({
            'message': message
        }))

    def _save_message(self , message):

        user_id = self.request.user.id
        user_name = self.request.user.username
        aritcle_id = self.request.path.split('/').pop(4)
        article_info = Article.objects.order_by('id').filter(id=aritcle_id)
        for article in article_info:
            company_info = Company.objects.filter(id=article.company_id)
            for info in company_info:
                
                self.model.objects.create(
                    company_id=info.id,
                    user_id=user_id,
                    article_id = article_id,
                    chat=message,
                    to_person=info.company_name,
                    form_person=user_name,
                )