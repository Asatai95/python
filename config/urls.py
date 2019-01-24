from django.conf.urls import url
from django.contrib.auth import views, urls
from django.urls import path, include
import mysite.views

from django.conf import settings
from django.conf.urls.static import static

import sys
import os

sys.path.append(os.getcwd() )
from mysite import chat

urlpatterns = [
    path('', include('mysite.urls')),
    path('', include('mysite.urls', namespace='apps')),
    path('', include('mysite.urls', namespace='register')),
    path('ws/chat/', include("mysite.chat.urls", namespace='chatroom')),
    path('jet/', include('jet.urls', 'jet')),
    path('register/', include('django.contrib.auth.urls')),
    path('index/', mysite.views.Index, name='index' ),
    # path('auth/', include('social_django.urls', namespace='social')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
