"""
Django settings for kwk project.
Generated by 'django-admin startproject' using Django 3.0.4.
For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import json
import pyrebase

DEV_ENV = True
TEST_ENV = False

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ''

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_crontab',
    'rest_framework',
    'utilities',
    'authModule',
    'seller',
    'buyer',
    'driver',
    'storages',
    'corsheaders',
    'payments',
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

ROOT_URLCONF = 'kwk.urls'

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


#CORS Settings
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

CORS_ALLOW_HEADERS = [
    'Access-Control-Allow-Origin',
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

WSGI_APPLICATION = 'kwk.wsgi.application'

if DEV_ENV:
    ConfigFile = os.path.join(BASE_DIR, 'kwk', 'project_settings.json')
elif TEST_ENV:
    ConfigFile = os.path.join(BASE_DIR, 'kwk', 'project_settings.json')
    
SettingInfo = ConfigFile
SettingInfo = open(SettingInfo, 'r')
SettingInfo = json.loads(SettingInfo.read())
Data = SettingInfo['data']
SettingInfo = Data['connectionString']
SettingInfo = SettingInfo.split(';')
SettingInfoDic = {}

for x in SettingInfo:
    if x != '':
        x = x.split('=')
        SettingInfoDic[x[0]] = x[1]

HostName = SettingInfoDic['Server']
UserId = SettingInfoDic['UserId']
Password = SettingInfoDic['Password']
Database = SettingInfoDic['Database']
Port = SettingInfoDic['Port']

MAX_UPLOAD_SIZE = Data['MAX_UPLOAD_SIZE']
IS_PRODUCTION = Data['IsProduction']
DEBUG = Data['Debug']


#Live Database (Do not remove/replace/migrate)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': Database,
        'USER': UserId,
        'PASSWORD': Password,
        'HOST':'',
        'PORT': Port
    }
}


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


#OTHER APPLICATION AND LIBRARIES CONFIGURATIONS

#Firebase Clouding Message
FCMDetails = Data['FIREBASEConfigurations']
#FCM_API_KEY = "AAAAOMOwU88:APA91bG-EwE-Bq5KsTfSZ57Eu2JyBRReeA2SF_jmVXQjMjW3h4KJG0qOl50rQ6H7b1bhUnO98QRta28rBg1hfG3dXNrMoEoNuLSv3USGHqYBSSTPA9Rhkj6vSiojlAG35I18Qsc2HYsv"
FCM_API_KEY = FCMDetails['FCM_API_KEY']

#Checkr Configurations
CHECKERDetails = Data['CHECKERConfigurations']
CHECKER_TEST_API_KEY = CHECKERDetails['CHECKER_TEST_API_KEY']
CHECKER_TEST_API_SECRET_KEY = CHECKERDetails['CHECKER_TEST_API_SECRET_KEY']
CHECKER_TEST_API_PUBLISHABLE_KEY = CHECKERDetails['CHECKER_TEST_API_PUBLISHABLE_KEY']
CHECKER_PACKAGE = CHECKERDetails['CHECKER_PACKAGE']
# CHECKER_PACKAGE = 'dunder_mifflin_executive'
# CHECKER_PACKAGE = 'driver_premium'

# TWILIO configurations
TWILIO_Details = Data['TWILIOConfigurations']
TWILIO_ACCOUNT_SID = TWILIO_Details['TWILIO_ACCOUNT_SID']
TWILIO_AUTH_TOKEN = TWILIO_Details['TWILIO_AUTH_TOKEN']
TWILIO_NUMBER = TWILIO_Details['TWILIO_NUMBER']
# SMS_BROADCAST_TO_NUMBERS = [ 
#     "+17722223450", # use the format +19735551234
# ]

# Email Settings
EMAIL_Details = Data['EmailConfigurations']
EMAIL_BACKEND = EMAIL_Details['EMAIL_BACKEND']
EMAIL_HOST_USER = EMAIL_Details['EMAIL_HOST_USER']
EMAIL_HOST = EMAIL_Details['EMAIL_HOST']
EMAIL_PORT = EMAIL_Details['EMAIL_PORT']
EMAIL_USE_TLS = EMAIL_Details['EMAIL_USE_TLS']
EMAIL_HOST_PASSWORD = EMAIL_Details['EMAIL_HOST_PASSWORD']

#AWS Configuarations
AWS_Details = Data['AWSCredentials']
AWS_S3_ACCESS_KEY_ID = AWS_Details['AWS_S3_ACCESS_KEY_ID']
AWS_S3_SECRET_ACCESS_KEY = AWS_Details['AWS_S3_SECRET_ACCESS_KEY']
AWS_STORAGE_BUCKET_NAME = AWS_Details['AWS_STORAGE_BUCKET_NAME']
AWS_S3_REGION_NAME = AWS_Details['AWS_S3_REGION_NAME']
AWS_S3_HOST = AWS_Details['AWS_S3_HOST']

#STRIPE Configurations
STRIP_Details = Data['STRIPEConfigurations']
STRIP_PUBLICATION_KEY = STRIP_Details['STRIP_PUBLICATION_KEY']
STRIP_SECRET_KEY = STRIP_Details['STRIP_SECRET_KEY']


# static files
# STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_URL_PATH = "https://" + AWS_STORAGE_BUCKET_NAME + \
    ".s3-" + AWS_S3_REGION_NAME + ".amazonaws.com/"

STATIC_LOCATION = 'static'
STATICFILES_STORAGE = 'utilities.custom_storage.StaticStorage'
STATIC_URL = STATIC_URL_PATH + "static/"
PUBLIC_MEDIA_LOCATION = 'media'
MEDIA_URL = STATIC_URL_PATH + "media/"
DEFAULT_FILE_STORAGE = 'utilities.custom_storage.PublicMediaStorage'


# media files configurations
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# STATIC_ROOT = os.path.join(BASE_DIR, "static/")
# MEDIA_ROOT = os.path.join(BASE_DIR, "media/")




# ASGI Application
ASGI_APPLICATION = 'kwk.asgi.application'
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('', 6379)],
        },
    },
}

CRONJOBS = [
    # ('5 0 * * *', 'authModule.cron_jobs.notified_on_expire_license'),

    ('1 * * * *', 'authModule.cron_jobs.notified_on_expire_license'),
    ('1 * * * *', 'authModule.cron_jobs.notified_on_expire_insurance'),
    ('*/1 * * * *', 'authModule.cron_jobs.email_otp_code_expiry'),
    ('*/1 * * * *', 'authModule.cron_jobs.phone_number_otp_code_expiry'),
    ('*/1 * * * *', 'authModule.cron_jobs.find_driver_nearby_buyer_for_order'),
]

#For Firebase JS SDK v7.20.0 and later, measurementId is optional
FIREBASE_CONFIG = {
  "apiKey": "",
  "authDomain": "",
  "databaseURL": "",
  "projectId": "",
  "storageBucket": "",
  "messagingSenderId": "",
  "appId": "",
  "measurementId": ""
};
FIREBASE = pyrebase.initialize_app(FIREBASE_CONFIG)
FIREBASE_AUTH = FIREBASE.auth()
FIREBASE_DATABASE = FIREBASE.database()
