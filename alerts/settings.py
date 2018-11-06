"""Alerts app settings."""

from django.conf import settings
from django.utils.dateparse import parse_time

# Control whether the worker should start
ACTIVE = getattr(settings, 'ALERTS_ACTIVE', False)
RUN_TIME = parse_time(getattr(settings, 'ALERTS_RUN_TIME', '08:00:00'))
MAIL_FROM = getattr(settings, 'ALERTS_MAIL_FROM', 'alerts@uptv.herokuapp.com')
