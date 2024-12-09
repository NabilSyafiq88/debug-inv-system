"""
Django settings for inventory_system project.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os
import dj_database_url
import psycopg2
import django_heroku

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Tell Django to use custom model instead of default one
AUTH_USER_MODEL = 'inventoryapp.CustomUser'


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'debug-inventory-system-hzf*2_8$xc$z0v%d@%$y=pqk_zwhmb^rl+ct+@m$i@q_-)wei)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
ALLOWED_HOSTS = ['*','debug-inventory-system-57b97c115148.herokuapp.com']
#ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'inventoryapp'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'inventory_system.urls'

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

WSGI_APPLICATION = 'inventory_system.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

#DATABASES = {
    #"default": {
        #'ENGINE': 'django.db.backends.sqlite3',
        #'NAME': BASE_DIR / 'db.sqlite3',
        ##"ENGINE": "django.db.backends.postgresql",
        ##"NAME": "d6c55e4t4me37j",
        ##"USER": "u536u1hmtptckr",
        ##"PASSWORD": "pa87a1850e63fcc4f68a4216bf1e5e5aaf103d15f92536d540cc1dcb1faef1fc8",
        ##"HOST": "localhost",
        ##"PORT": "5432",
    #}
#}



#DATABASE_URL = os.getenv('DATABASE_URL')
#conn = psycopg2.connect(DATABASE_URL, sslmode='require')

#print(DATABASE_URL)

#DATABASES['default'] = dj_database_url.config(default='postgres://u536u1hmtptckr:pa87a1850e63fcc4f68a4216bf1e5e5aaf103d15f92536d540cc1dcb1faef1fc8@ceqbglof0h8enj.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/d6c55e4t4me37j', test_options={'NAME': 'mytestdatabase'})

#DATABASES = {}
#DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)

#DATABASES = {}
#DATABASES['default'] = dj_database_url.config(default=os.getenv('DATABASE_URL'))

###DATABASES = {
    ###"default": {
        ###"ENGINE": "django.db.backends.postgresql",
        ###"USER": "u536u1hmtptckr",
        ###"NAME": "d6c55e4t4me37j",
        ###"TEST": {
            ###"NAME": "mytestdatabase",
        ###},
    ###},
###}

###DATABASES['default'] = dj_database_url.config('postgres://u536u1hmtptckr:pa87a1850e63fcc4f68a4216bf1e5e5aaf103d15f92536d540cc1dcb1faef1fc8@ceqbglof0h8enj.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/d6c55e4t4me37j')

##*FOR MASTER

DATABASES = { 
    'default': { 
        'ENGINE': 'django.db.backends.postgresql_psycopg2', 
        'NAME': 'd6c55e4t4me37j', 
        'USER': 'u536u1hmtptckr', 
        'PASSWORD': 'pa87a1850e63fcc4f68a4216bf1e5e5aaf103d15f92536d540cc1dcb1faef1fc8', 
        'HOST': 'ceqbglof0h8enj.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com', 
        'PORT': '5432', 
    } 
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kuala_Lumpur'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT =os.path.join(BASE_DIR, 'staticfiles')
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

##*MASTER
django_heroku.settings(locals())

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
