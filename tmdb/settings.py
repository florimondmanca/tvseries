"""TMDB client settings."""

from django.conf import settings

API_KEY = getattr(settings, 'TMDB_API_KEY', None)
TIME_ZONE = getattr(settings, 'TIME_ZONE', None)
