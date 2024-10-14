import environ

from .base import *

DEBUG = True

# Initialize environ
env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

SECRET_KEY = str(env('SECRET_KEY'))
