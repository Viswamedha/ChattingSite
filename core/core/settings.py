from pathlib import Path
from decouple import Csv, config
from dj_database_url import parse as db_url
import os 

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default = True, cast = bool)
ALLOWED_HOSTS = ['*']#config('ALLOWED_HOSTS', default = '127.0.0.1', cast = Csv(str))

INSTALLED_APPS = [
    # Default Django Apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # My Apps
    'main',
    'countries',
    'chat',
    # 3rd Party Apps
    'channels'
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

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
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

DATABASES = {
    'default': config(
        'DB_URL',
        default = 'sqlite:///db.sqlite3',
        cast = db_url
    )
}

WSGI_APPLICATION = 'core.wsgi.application'
ASGI_APPLICATION = 'core.asgi.application'

LANGUAGE_CODE = 'en-uk'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

AUTH_USER_MODEL = 'main.User'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

ROOT_URLCONF = 'core.urls'

STATIC_URL = '/static/'
# STATIC_ROOT = 'static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static', 
]

MEDIA_URL = '/media/'
MEDIA_ROOT = '/media/'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST', default = 'localhost')
EMAIL_PORT = config('EMAIL_PORT', default =  25, cast = int)
EMAIL_HOST_USER = config('EMAIL_HOST', default = '')
EMAIL_HOST_PASSWORD = config('EMAIL_PASS', default = '')
EMAIL_USE_TLS = config('EMAIL_TLS', default = False, cast = bool)

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("localhost", 6379)],
        },
    },
    "defaults": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}

    
