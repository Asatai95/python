from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base

from config import *

import os
import sys

from django import *
from django.contrib.messages import *
from django.contrib import *

from django.db import models
# from django.contrib.auth import get_user_model

sys.path.append(os.getcwd())
import facebook.custom_backends


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PROJECT_NAME = os.path.basename(BASE_DIR)

SECRET_KEY = '75c6@w6i1c=xsb$($_117$zk-v!@n*5r9(@tgcj+n=jj+ff*g!'

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

INSTALLED_APPS = [

    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'mysite.apps.WebappConfig',
    'mysite',
    'social_django',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
]

AUTHENTICATION_BACKENDS = [
    'social_core.backends.open_id.OpenIdAuth',
    'social_core.backends.google.GoogleOpenId',
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.google.GoogleOAuth',
    'django.contrib.auth.backends.ModelBackend',
    # 'facebook.custom_backends.SettingsBackend',
    'social_core.backends.facebook.FacebookOAuth2',

]

SESSION_COOKIE_SAMESITE = None


sys.path.append(os.getcwd())

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [os.path.join(BASE_DIR, "templates")],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                    'django.template.context_processors.static',
                    'social_django.context_processors.backends',
                    'social_django.context_processors.login_redirect',
                ],
            },
        },
    ]

LOGIN_URL = 'register:login'

LOGIN_REDIRECT_URL = 'register:top'
LOGOUT_URL = 'register:login'

sys.path.append(os.getcwd())
WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'roomii_sample',
        'USER': 'root',
        'PASSWORD': 'Asatai951156',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


TIME_ZONE = 'Asia/Tokyo'

LANGUAGE_CODE = 'ja'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_ROOT = '/var/www/{}/static'.format(PROJECT_NAME)
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_ROOT = '/var/www/{}/media/'.format(PROJECT_NAME)

AUTH_USER_MODEL = 'mysite.User'

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '296444933687-c11pj3e6ul0kj7utrj8smt34c3muq5jj.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'qGNbZlINKiAeaTxko6JZV-If'

# SOCIAL_AUTH_FACEBOOK_APP_NAMESPACE = 'auth'
SOCIAL_AUTH_FACEBOOK_KEY = '292183621408680'
SOCIAL_AUTH_FACEBOOK_SECRET = '1077fcc7e686d3c4ff08fbb05fcc94ab'
# SOCIAL_AUTH_FACEBOOK_SCOPE =  ['email', 'public_profile']
# SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
#   'fields': 'id,name,email'
# }


EMAIL_HOST = 'smtp.muumuu-mail.com'
DEFAULT_FROM_EMAIL = 'official@webapp2.com'
EMAIL_HOST_USER = 'official@webapp2.com'
EMAIL_HOST_PASSWORD = 'asatai951156'
EMAIL_PORT = 587
EMAIL_USE_TLS = False

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
