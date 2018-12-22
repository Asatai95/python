
from django.urls import path, include, re_path
from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required

from django.conf import settings
from django.conf.urls.static import static



app_name = 'mysite'

# url(r'^books/$', 'yourviewname', name='book_search')

urlpatterns = [
    path('login/', views.Login.as_view(), name='login'),
    # path('customer/login/', views.LoginCustomer.as_view(), name='customer_login'),
    path('logout/', login_required(views.Logout.as_view()), name='logout'),
    path('login_after/', views.LoginAfter.as_view(), name='login_after'),
    path('roomii/', login_required(views.MainView.as_view()), name='top'),
    path('roomii/', login_required(views.MainView.post), name='get_ajax'),
    url(r'^roomii/[0-9]', login_required(views.Redirect), {'location':'fab'}),
    # url(r'^roomii/', login_required(views.Redirect), {'location':'fab'}),
    # path('customer/roomii/', login_required(views.MainCustomerView.as_view()), name='customer_top'),
    path('user_create/', views.UserCreate.as_view(), name='user_create'),
    path('user_create/done/', views.UserCreateDone.as_view(), name='user_create_done'),
    path('user_create/complete/<token>/', views.UserCreateComplete.as_view(), name='user_create_complete'),
    path('password_change/', views.PasswordChange.as_view(), name='password_change'),
    path('password_change/done/', views.PasswordChangeDone.as_view(), name='password_change_done'),
    path('password_reset/', views.PasswordReset.as_view(), name='password_reset'),
    path('password_reset/done/', views.PasswordResetDone.as_view(), name='password_reset_done'),
    path('password_reset/confirm/<uidb64>/<token>/', views.PasswordResetConfirm.as_view(), name='password_reset_confirm'),
    path('password_reset/complete/', views.PasswordResetComplete.as_view(), name='password_reset_complete'),
    path('user_detail/<int:pk>/', login_required(views.UserDetail.as_view()), name='user_detail'),
    path('user_update/<int:pk>/', login_required(views.UserUpdate.as_view()), name='user_update'),
    path('roomii/info/<int:article_id>', login_required(views.InfoView.as_view()), name='info'),
    path('roomii/create/', login_required(views.ArticleEdit.as_view()), name='create'),
    path('roomii/update/<int:pk>', login_required(views.ArticleUpdate.as_view()), name='update'),
    path('google/login/', views.RedirectGoogle.as_view(), name='google_login'),
    path('auth/complete/google-oauth2/', views.Accesstoken.as_view(), name='google_callback'),
    path('facebook/login/', views.RedirectFacebook.as_view(), name='facebook_login'),
    path('auth/complete/facebook/', views.CallbackFacebook.as_view(), name='facebook_callback'),
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
