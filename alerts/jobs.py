import logging
import threading

from series.models import APIShow
from tmdb.client import tmdb_client


class AiringShowsJob(threading.Thread):
    """Job to fetch shows airing today and notify users that follow them.

    Usage
    -----
    Intended to be used as a regular thread:
    >>> job = AiringShowsJob()
    >>> job.start()
    >>> job.join()

    Logs
    ----
    Debug logs are available on the `alerts` logger (see `LOGGING` in
    settings.py).
    """

    _logger = logging.getLogger('alerts')

    def notify_followers(self, show: APIShow):
        for user in show.followers.all():
            # TODO send an email
            self._logger.debug({
                'event': 'alert_sent',
                'user': user.pk,
                'show': show.pk,
            })

    def run(self):
        self._logger.info({
            'event': 'started',
        })

        all_airing_today_ids = tmdb_client.get_airing_today_ids()
        saved_airing_today = APIShow.objects.filter(id__in=all_airing_today_ids)

        self._logger.debug({
            'all': all_airing_today_ids,
            'in_database': list(saved_airing_today.values_list(
                'id', flat=True
            )),
            'count': len(saved_airing_today),
        })

        if saved_airing_today:
            self._logger.info({
                'event': 'start_sending_alerts',
            })

        for show in saved_airing_today:
            self.notify_followers(show)

        self._logger.info({
            'event': 'done',
        })
