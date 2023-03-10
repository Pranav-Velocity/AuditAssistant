"""
Django settings for auditapp project.

Generated by 'django-admin startproject' using Django 3.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
from decimal import Decimal
from django.conf import global_settings
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ebfb1n_hc@=$c=y__e0=uw6#sjl&_$d5z8mb6thw8(o40g)k&g'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
LOCAL = False
ALLOWED_HOSTS = ['*']

LOGIN_REDIRECT_URL = '/'

LOGOUT_REDIRECT_URL = '/'


# Application definition


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'auditapp',
    'main_client',
    'partner',
    'manager',
    'auditor',
    'articleholder',
    'dev_admin',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware'
]

ROOT_URLCONF = 'auditapp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries': { # Adding this section should work around the issue.
                'static' : 'django.templatetags.static',
                'add_days': 'partner.templatetags.partner_extras'
            },
        },
    },
]

WSGI_APPLICATION = 'auditapp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
       'NAME': 'audit_test_3',
        'HOST': 'localhost',
        'PORT': '3306',
        'USER': 'root',
        'PASSWORD': 'root',
    
    }
}
# if LOCAL:
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.mysql',
#             'NAME': 'DHomcPe4Ay',
#             'USER': 'root',
#             'PASSWORD': '',
#             'HOST': '127.0.0.1',
#             'PORT': '3306',
#             'OPTIONS': {
#                 'sql_mode': 'STRICT_ALL_TABLES'
#             }
#         }
#     }
# else:
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.mysql',
#             'NAME': 'sharpeff_devauditassistant',
#             'USER': 'sharpeff_devauditassistantuser',
#             'PASSWORD': 'PQZ+wnn@(zm9',
#             'HOST': '127.0.0.1',
#             'PORT': '3306',
#             'OPTIONS': {
#                 'sql_mode': 'STRICT_ALL_TABLES'
#             }
#         }
#     }


# if LOCAL:
#    DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#        'NAME': 'django1',
#         'HOST': 'localhost',
#         'PORT': '3306',
#         'USER': 'root',
#         'PASSWORD': 'root',
    
# }
#     }
# else:
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.mysql',
#             'NAME': 'sharpeff_theauditassistant',
#             'USER': 'sharpeff_theauditassistant',
#             'PASSWORD': 'vtk8HqrfWpjRD7N',
#             'HOST': '127.0.0.1',
#             'PORT': '3306',
#             'OPTIONS': {
#                 'sql_mode': 'STRICT_ALL_TABLES'
#             }
#         }
#     }


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'testdb',
#         'USER': 'root',
#         'PASSWORD': '',
#         'HOST': '127.0.0.1',
#         'PORT': '3306',
#         'OPTIONS': {
#             'sql_mode': 'STRICT_ALL_TABLES'
#         }
#     }
# }
AUTH_USER_MODEL = 'auditapp.User'

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "live-static-files", "static-root")
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "live-static-files", "media-root")

# Mail configuration
EMAIL_BACKEND ='django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'icraftsolution.com@gmail.com'
EMAIL_HOST_PASSWORD ='ouhrseruuebtntmv'
EMAIL_PORT = 587
EMAIL_USE_TLS = True



PAYU_CONFIG = {
    "merchant_key": '7rnFly',
    "merchant_salt": 'pjVQAWpA',
    "mode": "test",
    "success_url": "http://127.0.0.1:8000/main_client/paymentsuccess",
    "failure_url": "http://127.0.0.1:8000/main_client/paymentfailure"
}