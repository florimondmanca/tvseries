"""Production settings."""

import os
from .settings import *


ALLOWED_HOSTS = [
    # For local debugging
    'localhost',
    '127.0.0.1',
    '0.0.0.0',
    # Heroku
    'uptv.herokuapp.com',
]

SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = False
