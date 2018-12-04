from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base

from config import *

import os
import sys

from django import *
from django.contrib.messages import *
from django.contrib import *

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
    'mysite.apps.WebappConfig',
    'social.apps.django_app.default',
    'mysite.models',
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
    'django.contrib.auth.backends.ModelBackend',
    'social_core.backends.open_id.OpenIdAuth',
    'social_core.backends.google.GoogleOpenId',
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.google.GoogleOAuth',
    # 'social_core.backends.facebook.FacebookOAuth2',
]

SESSION_COOKIE_SAMESITE = None


# SESSION_COOKIE_SECURE = True

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

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/index/'
LOGOUT_URL = '/index/'

sys.path.append(os.getcwd())
WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'roomii',
        'USER': 'root',
        'PASSWORD': 'Asatai951156',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

DATABASE = 'mysql://%s:%s@%s/%s?charset=utf8mb4' % (
       "root",
       "Asatai951156",
       "127.0.0.1:3306",
       "roomii",
    )

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


MEDIA_URL = '/img/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'static/img')
MEDIA_ROOT = '/var/www/{}/static/img'.format(PROJECT_NAME)

ENGINE = create_engine(
    DATABASE,
    encoding = "utf8",
    echo = True,
    pool_pre_ping = True,
)

session = scoped_session(
        sessionmaker(
            autocommit = False,
            autoflush = False,
            bind = ENGINE,
            )
        )


Base = declarative_base()
Base.query = session.query_property()

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '296444933687-kqqb70df90scmclga7ure2v1t8502rjb.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '2KuvRwHi0OLoc_h07cIQr7PE'
