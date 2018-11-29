from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

app_name = 'mysite'

urlpatterns = [
    path('index/', views.Index, name='index'),
    path('register/', views.Register, name='register'),
    path('confirm/', views.Confirm, name='confirm'),
    path('login/', views.Login, name='login'),
    path('users/mypage/', views.Mypage, name='mypage'),
    path('facebook/login/', views.Facebook, name='facebook'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
