from django.apps import AppConfig


class AlertsConfig(AppConfig):
    name = 'alerts'

    def ready(self):
        # NOTE: cannot be imported at module-level,
        # because importing this will trigger import of models that are
        # only ready when all apps have been loaded.
        # Example error:
        # "django.core.exceptions.AppRegistryNotReady: Apps aren't loaded yet."
        from alerts.worker import AlertWorker

        # NOTE: in development, Django runs two processes:
        # - One for the development server
        # - One for the auto-reload mechanism
        # Which results in this method being called twice.
        # It's probably fine and will not happen in production.
        # See:
        # https://stackoverflow.com/questions/33814615/how-to-avoid-appconfig-ready-method-running-twice-in-django
        worker = AlertWorker()
        worker.start()
