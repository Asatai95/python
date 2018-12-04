
from django.urls import path, include
from . import views

from django.conf import settings
from django.conf.urls.static import static

app_name = 'mysite'

urlpatterns = [
    # path('index/', views.Index, name='index'),
    path('register/', views.Register, name='register'),
    path('confirm/', views.Confirm, name='confirm'),
    path('login/google/', views.GoogleLogin, name='google'),
    path('auth/complete/google-oauth2/', views.GoogleCallBack, name='GoogleCallBack'),
    path('facebook/login/', views.FacebookLogin, name='facebook'),
    path('callback/facebook/', views.FacebookCallBack, name='FacebookCallBack'),
    path('login/', views.Login, name='login'),
    path('logout/', views.Logout, name='logout'),
    path('users/mypage/', views.Mypage, name='mypage'),
    path('users/mypage/edit/', views.MypageEdit, name='mypageedit'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
