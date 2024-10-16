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
