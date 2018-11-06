import sys
from django.apps import AppConfig


class AlertsConfig(AppConfig):
    name = 'alerts'

    def _worker_should_start(self) -> bool:
        """Return whether an alerts worker should start."""
        # NOTE: in development, Django runs two *processes* (not threads):
        # - One for the development server
        # - One for the auto-reload mechanism
        # Which results in the `ready()` method being called twice.
        # See:
        # https://stackoverflow.com/questions/33814615/how-to-avoid-appconfig-ready-method-running-twice-in-django
        # We *cannot* use a lock to check whether a worker is already
        # running, because this is a multiprocessing issue.
        # As a workaround, we require to deactivate auto-reload:
        # $ python manage.py runserver --noreload

        # Still, the worker should NOT start when performing operations
        # such as `manage.py test` or `manage.py migrate`.
        # It should only start in one of these cases:
        # 1) The server has started without `manage.py` (i.e. from gunicorn)
        # 2) The server has started with `manage.py runserver --noreload`

        from . import settings
        if sys.argv:
            if 'manage.py' not in sys.argv[0]:
                return settings.ACTIVE
            if sys.argv[1:] == ['runserver', '--noreload']:
                return settings.ACTIVE

        return False

    def ready(self):
        # NOTE: should not be imported at module-level,
        # because it would trigger an import of models that are
        # only ready when all apps have been loaded and raise the following:
        # "django.core.exceptions.AppRegistryNotReady: Apps aren't loaded yet."
        from alerts.worker import AlertsWorker
        if self._worker_should_start():
            worker = AlertsWorker()
            worker.start()
