from django.apps import AppConfig


class AlertsConfig(AppConfig):
    name = 'alerts'

    def ready(self):
        # NOTE: should not be imported at module-level,
        # because it would trigger an import of models that are
        # only ready when all apps have been loaded and raise the following:
        # "django.core.exceptions.AppRegistryNotReady: Apps aren't loaded yet."
        from alerts.worker import AlertWorker
        from . import settings

        # NOTE: in development, Django runs two processes:
        # - One for the development server
        # - One for the auto-reload mechanism
        # Which results in this method being called twice.
        # It's probably fine and will not happen in production.
        # See:
        # https://stackoverflow.com/questions/33814615/how-to-avoid-appconfig-ready-method-running-twice-in-django

        if settings.ACTIVE:
            worker = AlertWorker()
            worker.start()
