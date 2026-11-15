
import json
import os
from pathlib import Path

                                                                
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = BASE_DIR / 'templates'


                                                              
                                                                       

                                                                  
SECRET_KEY = 'django-insecure-w43w%gf&nchtr-veqmex$yem8jrvl!7i^!cjc%a!t(puab+3e!'

                                                                 
DEBUG = True

ALLOWED_HOSTS = []


                        

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cuentas',
    'experiencias',
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'inventarioAventura.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'inventarioAventura.wsgi.application'


          
                                                               

import pymysql
pymysql.install_as_MySQLdb()

database_config_path = BASE_DIR / 'database.local.json'
database_config = json.loads(database_config_path.read_text(encoding='utf-8')) if database_config_path.exists() else {}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME', database_config.get('NAME', 'aventura_db')),
        'USER': os.environ.get('DB_USER', database_config.get('USER', 'admin')),
        'PASSWORD': os.environ.get('DB_PASSWORD', database_config.get('PASSWORD', '')),
        'HOST': os.environ.get('DB_HOST', database_config.get('HOST', 'localhost')),
        'PORT': os.environ.get('DB_PORT', database_config.get('PORT', '3306')),
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


                      
                                                    

LANGUAGE_CODE = 'es-cl'

TIME_ZONE = 'America/Santiago'

USE_I18N = True

USE_TZ = True


                                        
                                                           

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]


LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'inicio'
LOGOUT_REDIRECT_URL = 'login'
