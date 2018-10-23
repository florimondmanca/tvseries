"""Long-running worker that executes alerting jobs."""
import logging
import threading

from alerts.jobs import AiringShowsJob

ONE_DAY = 60 * 60 * 24


class AlertWorker(threading.Thread):
    """Check for airing jobs every day.

    Notes
    -----
    Controlling the update time of day is not yet supported.
    The alerting job will be executed every day at the time
    that this thread is started.
    """

    period_seconds = ONE_DAY
    _logger = logging.getLogger('alerts')

    @staticmethod
    def main_thread_is_alive() -> bool:
        """Check if the main thread is still running.

        This check is required because the web server may not be able
        to correctly stop this thread and the Timer it has fired.
        """
        for thread in threading.enumerate():
            if thread.getName().find('MainThread') != -1:
                return thread.is_alive()
        return False

    def schedule_next(self):
        """Schedule another run of this job after the configured period."""
        return threading.Timer(self.period_seconds, lambda: self.run())

    def run(self):
        if not self.main_thread_is_alive():
            self._logger.info('Skipping because main thread has exited.')
            return

        job = AiringShowsJob()
        timer = self.schedule_next()

        job.start()
        timer.start()

        job.join()
        timer.join()
