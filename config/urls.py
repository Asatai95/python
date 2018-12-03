from django.conf.urls import url
from django.contrib.auth import views
from django.urls import path, include
import mysite.views

from django.conf import settings
from django.conf.urls.static import static

import sys
import os

urlpatterns = [
    path('', include('mysite.urls') ),
    path('index/', mysite.views.Index, name='index' ),
    path('facebook/login/', mysite.views.FacebookLogin, name='facebook' ),
    path('auth/', include('social_django.urls', namespace='social')),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
