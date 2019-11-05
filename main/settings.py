"""
Django settings for dlserver project.

Generated by 'django-admin startproject' using Django 1.11.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import socket

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*nqbimelq553&@0q7&ydkwe*2fbmb6#1%*xibu@-@%u0u@+dw@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

if DEBUG:
    ALLOWED_HOSTS = ['*']
else:
    ALLOWED_HOSTS = ['ai.aicvs.top', 'ai.aicvs.cn']

# Application definition

INSTALLED_APPS = [
    'django_crontab',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'django_filters',
    'goods',
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

ROOT_URLCONF = 'main.urls'

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'main.pagination.MyPageNumberPagination',
    'PAGE_SIZE': 50,
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',)
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'main.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

# def get_host_ip():
#     try:
#         s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#         s.connect(('8.8.8.8', 80))
#         ip = s.getsockname()[0]
#     finally:
#         s.close()
#
#     return ip
#
# my_host_ip =  get_host_ip()
#
# # TODO need remove
# if my_host_ip == '192.168.1.73':
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'goodsdl',
        'USER': 'gpu_rw',
        'PASSWORD': 'jyrMnQR1NdAKwgT4',
        'HOST': '10.19.68.63',
        'PORT': '3306',
        'CHARSET': 'utf8',
        'COLLATION': 'utf8_general_ci',
    },
    'ucenter': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ucenter',
        'USER': 'fx_ro',
        'PASSWORD': 'G8wN4RuZ2tJAuDa9',
        'HOST': 'udb-ucenter-m-1.xianlife.top',
        'PORT': '3306',
        'CHARSET': 'utf8',
        'COLLATION': 'utf8_general_ci',
    },
    'dmstore': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dmstore',
        'USER': 'readonly',
        'PASSWORD': 'fxiSHEhui2018@)@)',
        'HOST': '123.103.16.19',
        'PORT': '3300',
        'CHARSET': 'utf8',
        'COLLATION': 'utf8_general_ci',
    },
    'erp': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ls_diamond',
        'USER': 'diamond_ro',
        'PASSWORD': 'IW2MPdRYeliKdgue',
        'HOST': 'udb-diamond-m-1.xianlife.top',
        'PORT': '3306',
        'CHARSET': 'utf8',
        'COLLATION': 'utf8_general_ci',
    }
}
# else:
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.sqlite3',
#             'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#         }
#     }

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

# USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

UC_PIC_HOST = 'http://lximages.xianlife.com/'
DATASET_DIR_NAME = 'dataset'
DETECT_DIR_NAME = 'images'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },  # 针对 DEBUG = True 的情况
    },
    'formatters': {
        'standard': {
            # 'format': '%(levelname)s %(asctime)s %(pathname)s %(lineno)d: %(message)s'
            'format': '%(levelname)s %(asctime)s: %(message)s'
        },  # 对日志信息进行格式化，每个字段对应了日志格式中的一个字段，更多字段参考官网文档，我认为这些字段比较合适，输出类似于下面的内容
        # INFO 2016-09-03 16:25:20,067 /home/ubuntu/mysite/views.py views.py views get 29: some info...
    },
    'handlers': {
        'request_file_handler': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, "logs", 'debug.log'),
            'maxBytes': 1024 * 1024 * 50,  # 文件大小
            'backupCount': 50,  # 备份份数
            'formatter': 'standard'
        },  # 用于文件输出
        'detect_file_handler': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, "logs", 'detect.log'),
            'maxBytes': 1024 * 1024 * 50,  # 文件大小
            'backupCount': 50,  # 备份份数
            'formatter': 'standard'
        },  # 用于文件输出
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'request_file_handler'],
            'level': 'DEBUG',
            'propagate': True  # 是否继承父类的log信息
        },  # handlers 来自于上面的 handlers 定义的内容
        'detect': {
            'handlers': ['console', 'detect_file_handler'],
            'level': 'DEBUG',
            'propagate': True  # 是否继承父类的log信息
        },  # handlers 来自于上面的 handlers 定义的内容

    }
}

# train setting
TRAIN_ROOT = os.path.join(BASE_DIR, 'train')
MODEL_ROOT = os.path.join(BASE_DIR, 'dl', 'model')
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

# 跨域增加忽略
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = ()

CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
    'VIEW',
)

CORS_ALLOW_HEADERS = (
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
)
