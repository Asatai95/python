from django.urls import path

from . import consumers


app_name = 'chat'


channels_path = [
    path('ws/chat/<int:pk>/<int:article_id>/', consumers.ChatConsumer),
]
