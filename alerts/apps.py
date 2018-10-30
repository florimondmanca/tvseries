from django.apps import AppConfig


class AlertsConfig(AppConfig):
    name = 'alerts'

    def ready(self):
        # NOTE: should not be imported at module-level,
        # because it would trigger an import of models that are
        # only ready when all apps have been loaded and raise the following:
        # "django.core.exceptions.AppRegistryNotReady: Apps aren't loaded yet."
        from alerts.worker import AlertsWorker
        from . import settings

        # NOTE: in development, Django runs two *processes* (not threads):
        # - One for the development server
        # - One for the auto-reload mechanism
        # Which results in this `ready()` method being called twice.
        # See:
        # https://stackoverflow.com/questions/33814615/how-to-avoid-appconfig-ready-method-running-twice-in-django
        # We *cannot* use a lock to check whether a worker is already
        # running, because this is a multiprocessing issue.
        # As a workaround, deactivate auto-reload:
        # $ python manage.py runserver --noreload
        if settings.ACTIVE:
            worker = AlertsWorker()
            worker.start()
