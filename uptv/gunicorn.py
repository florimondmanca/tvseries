"""Gunicorn production server configuration.

Documentation:
http://docs.gunicorn.org/en/stable/settings.html

Configuration example:
https://github.com/benoitc/gunicorn/blob/master/examples/example_config.py
"""

import os

# Only 1 worker should start (defaults to 3) because we do NOT want
# multiple instances of the alerts worker thread (which would result in
# multiple copies of emails being sent).
workers = 1

bind = f'0.0.0.0:{os.environ.get("PORT")}'
