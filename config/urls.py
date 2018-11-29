from django.conf.urls import url
from django.urls import path, include
from mysite import views

from django.conf import settings
from django.conf.urls.static import static

import sys
import os

urlpatterns = [
    path('', include('mysite.urls') ),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
