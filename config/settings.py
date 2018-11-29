from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base

import os
import sys

import django

FACEBOOK_ID = '333564927437881'
FACEBOOK_SECRET = 'da43ee4cd59781031fd6f98c85be5f51'
FACEBOOK_CALLBACK_URL = 'http://localhost:5000/facebook/callback'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PROJECT_NAME = os.path.basename(BASE_DIR)

SECRET_KEY = '75c6@w6i1c=xsb$($_117$zk-v!@n*5r9(@tgcj+n=jj+ff*g!'


DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'mysite.apps.WebappConfig',
    'mysite.models',
    'social_django',
]

SESSION_COOKIE_SECURE=None

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

sys.path.append('/var/www/django/config')

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

AUTHENTICATION_BACKENDS = [
    'social_core.backends.open_id.OpenIdAuth',
    'social_core.backends.google.GoogleOpenId',
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.github.GithubOAuth2',
    'social_core.backends.facebook.FacebookOAuth2',
    'django.contrib.auth.backends.ModelBackend',
]

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '296444933687-cepitheum60d4c87iit6ft46veqf92q9.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '8kaj-wfWDzDkK2fnzEVzPBYI'

LOGIN_REDIRECT_URL = '/index/'
SOCIAL_AUTH_URL_NAMESPACE = 'social'


sys.path.append('/var/www/django/config')

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


MEDIA_URL = '/media/'
MEDIA_ROOT = '/var/www/{}/media'.format(PROJECT_NAME)

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
