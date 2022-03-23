"""
Django settings for persia_atlas project.

Generated by 'django-admin startproject' using Django 3.2.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
from pathlib import Path
from datetime import timedelta
from decouple import config


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-fcgh&-e%4#(*cg_ih23@b6dd)lblnf7_@s+q92_vd-$#v7upj2'
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG')

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'persia-atlas.com', 'www.persia-atlas.com']

# Application definition

INSTALLED_APPS = [
    'users.apps.UsersConfig',
    'products.apps.ProductsConfig',
    'accounting.apps.AccountingConfig',

    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'django_filters',
    'drf_yasg',
    'celery',
    'django_celery_results',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'persia_atlas.urls'

TEMPLATES = [
    {
        'BACKEND':  'django.template.backends.django.DjangoTemplates',
        'DIRS':     [],
        'APP_DIRS': True,
        'OPTIONS':  {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'persia_atlas.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME':   BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE':   config('DB_ENGINE'),
        'NAME':     config('DB_NAME'),
        'HOST':     config('DB_HOST'),
        'USER':     config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'PORT':     config('DB_PORT'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = config('STATIC_ROOT')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

MEDIA_DIR_NAME = 'media'
MEDIA_ROOT = os.path.join(BASE_DIR, MEDIA_DIR_NAME)
MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'users.User'

CORS_ALLOWED_ORIGINS = [
    'http://localhost:8080',
    'http://localhost:3000',
    'https://persia-atlas.com'
]

# ******************* settings for DRF *******************
DEFAULT_RENDERER_CLASSES = [
    'rest_framework.renderers.JSONRenderer',
]

if DEBUG:
    DEFAULT_RENDERER_CLASSES += [
        'rest_framework.renderers.BrowsableAPIRenderer',
    ]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES':     [
        'rest_framework.permissions.IsAuthenticated',
        # 'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES':       DEFAULT_RENDERER_CLASSES,
    'DEFAULT_FILTER_BACKENDS':        (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_PAGINATION_CLASS':       'persia_atlas.drf.CustomPageNumberPagination',
}
# *********************************************************

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME':           timedelta(days=7),
    'REFRESH_TOKEN_LIFETIME':          timedelta(days=14),
    'ROTATE_REFRESH_TOKENS':           False,
    'BLACKLIST_AFTER_ROTATION':        True,
    'UPDATE_LAST_LOGIN':               False,

    'ALGORITHM':                       'HS256',
    'SIGNING_KEY':                     SECRET_KEY,
    'VERIFYING_KEY':                   None,
    'AUDIENCE':                        None,
    'ISSUER':                          None,
    'JWK_URL':                         None,
    'LEEWAY':                          0,

    'AUTH_HEADER_TYPES':               ('Bearer',),
    'AUTH_HEADER_NAME':                'HTTP_AUTHORIZATION',
    'USER_ID_FIELD':                   'id',
    'USER_ID_CLAIM':                   'user_id',
    'USER_AUTHENTICATION_RULE':        'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES':              ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM':                'token_type',

    'JTI_CLAIM':                       'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME':          timedelta(days=7),
    'SLIDING_TOKEN_REFRESH_LIFETIME':  timedelta(days=14),
}

DIGIKALA_LOGIN_URL = 'https://seller.digikala.com/account/login/?_back=https://seller.digikala.com/'
DIGIKALA_URLS = {
    'home':                  'https://seller.digikala.com/',
    'login':                 'https://seller.digikala.com/account/login/?_back=https://seller.digikala.com/',
    'profile':               'https://seller.digikala.com/profile/new/display/',
    'update_variant_data':   'https://seller.digikala.com/ajax/variants/inline/update/',
    'update_variant_status': 'https://seller.digikala.com/ajax/variants/inline/changeactivation/',
}

DIGIKALA_LOGIN_CREDENTIALS = {
    'login[email]':    config('DIGI_USERNAME'),
    'login[password]': config('DIGI_PASSWORD'),
    'remember':        True
}

MAX_DAYS_DELETE_COST = 3

GECKO_DRIVER_PATH = config('GECKO_DRIVER_PATH')

CELERY_RESULT_BACKEND = 'django-db'
CELERY_CACHE_BACKEND = 'django-cache'

CUSTOM_LOGGING = config('CUSTOM_LOGGING')