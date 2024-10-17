import os

import environ

from .base import *

DEBUG = True

ENVIRONMENT = 'development'

env = environ.Env(
    DEBUG=(bool, False)
)

environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

SECRET_KEY = str(env('SECRET_KEY'))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AWS_ACCESS_KEY_ID = str(env('AWS_ACCESS_KEY_ID'))
AWS_SECRET_ACCESS_KEY = str(env('AWS_SECRET_ACCESS_KEY'))
AWS_STORAGE_BUCKET_NAME = str(env('AWS_STORAGE_BUCKET_NAME'))
AWS_S3_REGION_NAME = str(env('AWS_S3_REGION_NAME'))
