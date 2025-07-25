import os
from datetime import timedelta
from pathlib import Path

from cryptography.fernet import Fernet
from redis import Redis

from hokm.redis import get_redis_client
from mongoengine import connect as mongo_connect

MONGO_CLIENT = mongo_connect(host=os.environ.get("MONGO_DB_URI"))


# EMAIL CONFIG
EMAIL_BACKEND = os.environ.get("EMAIL_BACKEND")
EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT"))
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS") == 'True'
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL")


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = os.environ.get('DEBUG', "False") == 'True'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

PROJECT_NAME = os.environ.get('PROJECT_NAME', "hokm")

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'storages',
    'rest_framework_simplejwt',
    'drf_yasg',
    "django_celery_results",
    "django_celery_beat",
    'user.apps.UserConfig',
    'common.apps.CommonConfig',
    'shop.apps.ShopConfig',
    'player_shop.apps.PlayerShopConfig',
    'social.apps.SocialConfig',
    'player_statistic.apps.PlayerStatisticConfig',
    'leaderboard.apps.LeaderboardConfig',
    'match.apps.MatchConfig'

]

# MINIO
AWS_ACCESS_KEY_ID = os.environ.get("MINIO_ROOT_USER")
AWS_SECRET_ACCESS_KEY = os.environ.get("MINIO_ROOT_PASSWORD")
AWS_STORAGE_BUCKET_NAME = os.environ.get("MINIO_BUCKET_NAME")
AWS_S3_ENDPOINT_URL = 'http://172.16.11.28:9000'
AWS_S3_USE_SSL = False
AWS_S3_SIGNATURE_VERSION = 's3v4'
AWS_S3_REGION_NAME = 'us-east-1'
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
AWS_S3_VERIFY = False

STORAGES = {
    "default": {
        "BACKEND": 'storages.backends.s3boto3.S3Boto3Storage',
        "OPTIONS": {
            'access_key': AWS_ACCESS_KEY_ID,
            'secret_key': AWS_SECRET_ACCESS_KEY,
            'bucket_name': AWS_STORAGE_BUCKET_NAME,
            'endpoint_url': AWS_S3_ENDPOINT_URL,
            'default_acl': None,
            'querystring_auth': True,
            'file_overwrite': False,
        },
    },
    'staticfiles': {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    }
}

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    },
    'USE_SESSION_AUTH': False,
    'JSON_EDITOR': True,
    'SUPPORTED_SUBMIT_METHODS': [
        'get',
        'post',
        'put',
        'delete',
        'patch'
    ],
    'OPERATIONS_SORTER': 'alpha',
    'TAGS_SORTER': 'alpha',
    'DOC_EXPANSION': 'none',
    'DEEP_LINKING': True,
    'SHOW_EXTENSIONS': True,
    'DEFAULT_MODEL_RENDERING': 'model',
}

REDOC_SETTINGS = {
    'LAZY_RENDERING': False,
}

AUTH_USER_MODEL = 'user.User'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'hokm.urls'

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

WSGI_APPLICATION = 'hokm.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('POSTGRES_DB', default=PROJECT_NAME),
        'USER': os.getenv('POSTGRES_USER', default='postgres'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', default='12345'),
        'HOST': os.getenv('POSTGRES_HOST', default='localhost'),
        'PORT': int(os.getenv('POSTGRES_PORT', default='5432')),
        'CONN_MAX_AGE': int(os.getenv('CONN_MAX_AGE', default=60)),
    }
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": os.environ.get('REDIS_URI', ""),
        "TIMEOUT": int(os.getenv('REDIS_TIMEOUT', default='3600')),
        "KEY_PREFIX": os.getenv('REDIS_KEY_PREFIX', default=PROJECT_NAME),
    }
}

CACHE_EXPT = {
    "otp": int(os.environ.get("OTP_EXPIRATION_TIME", "120"))
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

REDIS_CLIENT = get_redis_client()

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
USE_L10N = True

LANGUAGES = [
    ('en', 'English'),
    ('fa', 'Farsi'),
]

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

NEEDED_DIRS = [
    os.path.join(BASE_DIR, 'static'),
    os.path.join(BASE_DIR, 'temp'),
    os.path.join(BASE_DIR, 'media')
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': "rest_framework.pagination.PageNumberPagination",
    'PAGE_SIZE': int(os.getenv('DEFAULT_PAGE_SIZE', default=20)),
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=int(os.environ.get("ACCESS_TOKEN_LIFETIME", "5"))),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=int(os.environ.get("REFRESH_TOKEN_LIFETIME", "1"))),
    "AUTH_HEADER_TYPES": ("Bearer",),
}

CIPHER_SUITE = Fernet(os.environ.get("ENCRYPTION_KEY"))


for d in NEEDED_DIRS:
    if not os.path.isdir(d):
        os.mkdir(d)

STATIC_URL = f'/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
#
# MEDIA_URL = f'/media/'
#
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULTS_BACKEND")
