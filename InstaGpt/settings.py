"""
Django settings for InstaGpt project.

Generated by 'django-admin startproject' using Django 3.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
import environ

env = environ.Env()
environ.Env.read_env()
LIVE = env.bool('LIVE')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str('SECRET_KEY')
OPENGPTKEY = env.str('OPENGPTKEY')

# print(SECRET_KEY)
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG', default=False)

ALLOWED_HOSTS = ['*']
CSRF_TRUSTED_ORIGINS = ['https://webapi.chirpflo.com']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Signup',
    'Company',
    'adminapp',
    'rest_framework',
    'corsheaders',
    'drf_api_logger',
    'django_celery_results',
    "storages"
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'drf_api_logger.middleware.api_logger_middleware.APILoggerMiddleware',
]

ROOT_URLCONF = 'InstaGpt.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'InstaGpt.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

print(LIVE,"Settings")
# DATABASES={
#     'default': {         
#         'ENGINE': env.str('ENGINE'),        
#         'NAME': env.str('POSTGRESQL_DB'),         
#         'USER': env.str('POSTGRESQL_USER'),        
#         'PASSWORD': env.str('POSTGRESQL_PASSWORD'),
#         'HOST': env.str('POSTGRESQL_HOST'),
#         'PORT': env.str('POSTGRESQL_PORT'),
#     }
# }



if LIVE == True:    
    DATABASES = {
    'default': {
        #    'ENGINE': 'django.db.backends.postgresql',
        #    'NAME': 'postgres',
        #    'USER': 'postgres',
        #    'PASSWORD': 'postgres',
        #    'HOST': 'localhost',
        #    'PORT': 5432,

        'ENGINE': env.str('ENGINE'),
        'NAME': env.str('NAME'),
        'USER': env.str('USER'),
        'PASSWORD': env.str('PASSWORD'),
        'HOST': env.str('HOST'),
        'PORT': env.str('PORT'),
    }
    }
else:
    print("elseeeeee", env.str('LOCAL_DB_HOST'), env.str('LOCAL_DB_NAME'))
    DATABASES = {
    'default': {
            # 'ENGINE': 'django.db.backends.postgresql',
            # 'NAME': 'postgres',
            # 'USER': 'postgres',
            # 'PASSWORD': 'postgres',
            # 'HOST': 'localhost',
            # 'PORT': 5432,
            'ENGINE': env.str('ENGINE'),
            'NAME': env.str('LOCAL_DB_NAME'),
            'USER': env.str('LOCAL_POSTGRES_USER'),
            'PASSWORD': env.str('LOCAL_POSTGRES_PASSWORD'),
            'HOST': env.str('LOCAL_DB_HOST'),
            'PORT': env.str('LOCAL_DB_PORT'),
        }
    }




# Passwordvalidation
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

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL='Signup.User'
#================================================================
# JWT Configurations
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        # 'rest_framework.authentication.SessionAuthentication',

    ),
    # 'DEFAULT_PAGINATION_CLASS': 'Company.views.CustomPagination',
}
REST_USE_JWT = True
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=2),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': 'SECRET_KEY',
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}


SENDGRID_API_KEY = env.str('SENDGRID_API_KEY')
SENDGRID_EMAIL=env.str('SENDGRID_EMAIL')

CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
    "company",
    "locale",
    "Access-Control-Allow-Origin"
]

DRF_API_LOGGER_DATABASE = True  

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

#Celery backend Task
CELERY_ENABLED = True

# CELERY_BROKER_URL = "redis://localhost:6379"
# CELERY_RESULT_BACKEND = "redis://localhost:6379"

BROKER_URL = 'redis://127.0.0.1:6379'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Kolkata'
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

#AWS settings
AWS_ACCESS_KEY_ID = env.str('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env.str('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = env.str('AWS_STORAGE_BUCKET_NAME')
AWS_DEFAULT_ACL = 'public-read'
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}

WEB_URL=env.str('WEB_URL')