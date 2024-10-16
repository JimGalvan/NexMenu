
import os

import dj_database_url

from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = str(os.getenv('SECRET_KEY'))

ALLOWED_HOSTS = ['*']

ENVIRONMENT = 'production'

print("DATABASE_URL: ", os.getenv('DATABASE_URL'))
print("ENGINE: ", os.getenv('DB_ENGINE', default='django.db.backends.postgresql'))
print("NAME: ", os.getenv('DB_NAME'))
print("USER: ", os.getenv('DB_USER'))
print("PASSWORD: ", os.getenv('DB_PASSWORD'))
print("HOST: ", os.getenv('DB_HOST', default='localhost'))
print("PORT: ", os.getenv('DB_PORT', default='5432'))

DATABASES = {
    'default': dj_database_url.config(default=os.getenv('DATABASE_URL'))
}

CSRF_TRUSTED_ORIGINS = ['https://nexmenu-production.up.railway.app']

