"""Alerts app settings."""
from django.conf import settings

# Control whether the worker should start
ACTIVE = getattr(settings, 'ALERTS_ACTIVE', False)
