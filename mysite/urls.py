
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
    path('login/google/', views.GoogleLogin, name='google'),
    path('auth/complete/google-oauth2/', views.GoogleCallBack, name='GoogleCallBack'),
    path('login/facebook/', views.FacebookLogin, name='facebook'),
    path('auth/complete/callback/', views.FacebookCallBack, name='FacebookCallBack'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
