"""Production settings."""

import os
from .settings import *


ALLOWED_HOSTS = [
    'uptv.herokuapp.com',
]

SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = False
