
import os 
import sys

from django.urls import path, include, re_path
from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required

from django.conf import settings
from django.conf.urls.static import static 

app_name = 'mysite'

# url(r'^books/$', 'yourviewname', name='book_search')

urlpatterns = [
    path('', views.TopSearch.as_view(), name='top_search'),
    path('login/', views.Login.as_view(), name='login'),
    # path('customer/login/', views.LoginCustomer.as_view(), name='customer_login'),
    path('logout/', login_required(views.Logout.as_view()), name='logout'),
    path('login_after/', views.LoginAfter.as_view(), name='login_after'),
    path('roomii/', views.MainView.as_view(), name='top'),
    path('roomii/<urlpath>', views.MainView.as_view(), name='top_path'),
    path('roomii/', login_required(views.MainView.post), name='get_ajax'),
    path('user_create/', views.UserCreate.as_view(), name='user_create'),
    path('user_create/done/', views.UserCreateDone.as_view(), name='user_create_done'),
    path('user_create/complete/<token>/', views.UserCreateComplete.as_view(), name='user_create_complete'),
    path('password_change/', views.PasswordChange.as_view(), name='password_change'),
    path('password_change/done/', views.PasswordChangeDone.as_view(), name='password_change_done'),
    path('password_reset/', views.PasswordReset.as_view(), name='password_reset'),
    path('password_reset/done/', views.PasswordResetDone.as_view(), name='password_reset_done'),
    path('password_reset/confirm/<uidb64>/<token>/', views.PasswordResetConfirm.as_view(), name='password_reset_confirm'),
    path('password_reset/complete/', views.PasswordResetComplete.as_view(), name='password_reset_complete'),
    path('user_detail/<username>/<int:pk>/', login_required(views.UserDetail.as_view()), name='user_detail'),
    path('send/mail/<str:article_name>/', login_required(views.Send_email.as_view()), name='send_email'),
    path('user_update/<int:pk>/', login_required(views.UserUpdate.as_view()), name='user_update'),
    path('roomii/info/<int:article_id>/', (views.InfoView.as_view()), name='info'),
    path('roomii/info/<int:article_id>/<urlpath>/', (views.InfoView.as_view()), name='info_path'),
    path('roomii/create/', login_required(views.ArticleEdit.as_view()), name='create'),
    path('roomii/update/<int:pk>', login_required(views.ArticleUpdate.as_view()), name='update'),
    path("roomii/company/", login_required(views.CompanyView.as_view()), name='company'),
    path("roomii/company/update/", login_required(views.CompanyChange.as_view()), name='company_change'),
    path('google/login/', views.RedirectGoogle.as_view(), name='google_login'),
    path('auth/complete/google-oauth2/', views.Accesstoken.as_view(), name='google_callback'),
    path('facebook/login/', views.RedirectFacebook.as_view(), name='facebook_login'),
    path('auth/complete/facebook/', views.CallbackFacebook.as_view(), name='facebook_callback'),
    path('test_image/', views.image.as_view(), name='test_image'),
    path('plan/', login_required(views.Stripe.as_view()), name='stripe'),
    path('stripe/charge/<str:namespace>/', login_required(views.Charge.as_view()), name='charge'),
    path('test/', views.Insert.as_view(), name='test'),
    path('request/', login_required(views.Article_request.as_view()), name='article_request'),
    
    # path('mail_test/', views.Message_test.as_view(), name='message_get_info'),
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
