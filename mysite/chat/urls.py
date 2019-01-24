from django.conf.urls import url
from django.contrib.auth import views, urls
from django.urls import path, include

from django.contrib.auth.decorators import login_required

from django.conf import settings
from django.conf.urls.static import static

import sys
import os

from . import views

app_name = 'chat'

urlpatterns = [
    path('<int:pk>/<int:article_id>/', login_required(views.ChatView.as_view()), name='index'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
