"""Alerts app settings."""

from django.conf import settings

# Control whether the worker should start
from django.utils.dateparse import parse_time

ACTIVE = getattr(settings, 'ALERTS_ACTIVE', False)
RUN_TIME = parse_time(getattr(settings, 'ALERTS_RUN_TIME', '08:00:00'))
