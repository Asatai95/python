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

if os.environ.get("APP_ENVIRONMENT") == "production":
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    PROJECT_NAME = os.path.basename(BASE_DIR)

    SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")

    DEBUG = True

    ALLOWED_HOSTS = ['*']

    INSTALLED_APPS = [

       'django.contrib.auth',
       'django.contrib.contenttypes',
       'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        # 'mysite.apps.WebappConfig',
        'mysite',
        # 'social_django',
        'jet',
        'cloudinary',
        'cloudinary_storage',
        'mysite.chat',
        'channels',
    ]

    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels_redis.core.RedisChannelLayer",
            "CONFIG": {
                "hosts": [("localhost", 6379)],
            },
        },
    }

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]

    SESSION_ENGINE = 'django.contrib.sessions.backends.db'

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
                        
                    ],
                },
            },
        ]

    LOGIN_URL = 'register:login'

    LOGIN_REDIRECT_URL = 'register:login_after'
    LOGOUT_URL = 'register:logout'

    sys.path.append(os.getcwd())
    WSGI_APPLICATION = 'config.wsgi.application'

    sys.path.append(os.getcwd())
    ASGI_APPLICATION = 'mysite.routing.application'

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.environ.get("MySQL_TABLE_NAME"),
            'USER': 'root',
            'PASSWORD': os.environ.get("MySQL_PASSWORD"),
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


    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

    AUTH_USER_MODEL = 'mysite.User'

    SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.environ.get("SOCIAL_AUTH_GOOGLE_OAUTH2_KEY")
    SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.environ.get("SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET")

    FACEBOOK_CALLBACK_URL= os.environ.get("FACEBOOK_CALLBACK_URL")
    SOCIAL_AUTH_FACEBOOK_KEY = os.environ.get("SOCIAL_AUTH_FACEBOOK_KEY")
    SOCIAL_AUTH_FACEBOOK_SECRET = os.environ.get("SOCIAL_AUTH_FACEBOOK_SECRET")

    EMAIL_HOST = os.environ.get("EMAIL_HOST")
    DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL")
    EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
    EMAIL_PORT = os.environ.get("EMAIL_PORT")
    EMAIL_USE_TLS = False

    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

    DATABASE = 'mysql://%s:%s@%s/%s?charset=utf8mb4' % (
        "root",
        os.environ.get("MySQL_TABLE_NAME"),
        "127.0.0.1:3306",
        os.environ.get("MySQL_PASSWORD"),
    )

    ENGINE = create_engine(
        DATABASE,
        encoding = "utf8",
        echo=True,
        pool_pre_ping=True
    )

    session = scoped_session(
        sessionmaker(
            autocommit = False,
            autoflush = False,
            bind = ENGINE
            )
        )

    Base = declarative_base()
    Base.query = session.query_property()

    # CLOUDINARY_STORAGE = {
    #     'CLOUD_NAME': os.environ.get("CLOUD_NAME"),
    #     'API_KEY': os.environ.get("CLOUDINARY_STORAGE_API_KEY"),
    #     'API_SECRET': os.environ.get("CLOUDINARY_STORAGE_API_SECRET"),
    # }
    #
    # DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

    SESSION_SAVE_EVERY_REQUEST = True

    FILE_UPLOAD_MAX_MEMORY_SIZE = "10485760"

