from django.contrib.auth import views
from django.urls import path, include
from . import views

from django.conf import settings
from django.conf.urls.static import static

app_name = 'mysite'

urlpatterns = [
    path('register/', views.Register, name='register'),
    path('confirm/', views.Confirm, name='confirm'),
    path('login/', views.Login, name='login'),
    path('users/mypage/', views.Mypage, name='mypage'),
    path('index/', views.Index, name='index'),
    path('logout/', views.Logout, name='logout'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
