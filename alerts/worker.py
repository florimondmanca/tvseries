"""Long-running worker that executes alerting jobs."""
import logging
import threading
from datetime import time, timedelta, datetime
from time import sleep

from django.utils import timezone

from alerts.jobs import AiringShowsJob
from . import settings


class AlertsWorker(threading.Thread):
    """Check for airing jobs every day.

    Notes
    -----
    Controlling the update time of day is not yet supported.
    The alerting job will be executed every day at the time
    that this thread is started.
    """

    _logger = logging.getLogger('alerts')
    _poll_duration_seconds = 10

    @property
    def run_time(self) -> time:
        """Return the run time of the alerts worker."""
        return settings.RUN_TIME

    def seconds_to_next_run(self, dt: datetime) -> int:
        """Return the number of seconds between a date and the next run.

        :param dt: datetime
        :return delay : int
            Number of seconds between `dt` and the next run.
        """
        run_time = self.run_time

        # Compute the day of the next run.
        # It depends on whether the given time is before (same day),
        # or after (next day) the run time.
        if dt.time() < run_time:
            next_run_day = dt.date()
        else:
            next_run_day = dt.date() + timedelta(days=1)

        next_run = timezone.datetime.combine(
            date=next_run_day,
            time=run_time,
            tzinfo=dt.tzinfo,
        )

        delta: timedelta = next_run - dt
        delay = int(delta.total_seconds())

        return delay

    def _wait_for_next_run(self):
        """Wait for the next run of the worker."""
        delay = self.seconds_to_next_run(timezone.now())
        while delay > 0:
            self._logger.info({
                'event': 'checking_for_next_run',
                'seconds_to_next_run': delay,
            })
            chunk = min(delay, self._poll_duration_seconds)
            self._logger.info({
                'event': 'going_to_sleep',
                'duration': chunk,
            })
            sleep(chunk)
            delay -= chunk

    def _run_job(self):
        job = AiringShowsJob()
        job.daemon = True  # Kill if main thread exits
        job.start()
        job.join()

    def run(self):
        while self.is_alive():
            self._wait_for_next_run()
            self._run_job()
