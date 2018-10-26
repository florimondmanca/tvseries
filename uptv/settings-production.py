"""Production settings."""

from .settings import *
import os
import dj_database_url

ALLOWED_HOSTS = [
    # For local debugging
    'localhost',
    '127.0.0.1',
    '0.0.0.0',
    # Heroku
    'uptv.herokuapp.com',
]

SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = os.environ.get('DEBUG', False) or False

# SQLite is not available on Heroku (no access to persistent disk storage)
# => We use PostgreSQL
# dj_database_url expects a DATABASE_URL environment variable, to be
# configured on Heroku.
DATABASES['default'] = dj_database_url.config()
