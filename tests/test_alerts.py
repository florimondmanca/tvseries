from datetime import datetime, timedelta

from django.core import mail
from django.test import TestCase
from django.utils.timezone import now

from alerts.worker import AlertsWorker
from users.models import User
from series.models import APIShow
from alerts.notifications import EmailNotifier


class EmailTest(TestCase):
    """Email notification testing.
    
    Inspired from:
    https://docs.djangoproject.com/en/2.1/topics/testing/tools/#email-services
    """

    def test_send_email(self):
        # Add user and tv show
        user = User.objects.create_user(username='username', email='to@example.com', password='password')
        user.save()
        show = APIShow(id='1', title='Test TV Show')
        show.save()
        show.followers.add(user)

        notifier = EmailNotifier()
        notifier.notify(user, show)

        # Test that one message has been sent.
        self.assertEqual(len(mail.outbox), 1)

        # Verify that the subject of the first message is correct.
        self.assertEqual(mail.outbox[0].subject, notifier.get_subject())

        # Verify that the body of the first message is correct.
        self.assertEqual(mail.outbox[0].body, notifier._get_full_content(show))  # Private but just for the test


class NextRunTest(TestCase):
    """Test the computation of the next run in AlertsWorker."""

    def setUp(self):
        self.worker = AlertsWorker()

    def _today_run(self):
        return datetime.combine(now().date(), self.worker.run_time)

    def _get_delay_for_delta(self, delta: timedelta) -> int:
        dt = datetime.combine(now().date(), self.worker.run_time) + delta
        return self.worker.seconds_to_next_run(dt)

    def test_if_time_is_before_run_hour_then_is_amount_of_seconds(self):
        delay = self._get_delay_for_delta(timedelta(seconds=-10))
        self.assertEqual(delay, 10)

    def test_if_time_is_after_run_hour_then_is_amount_of_seconds_plus_one_day(self):
        delay = self._get_delay_for_delta(timedelta(seconds=10))
        one_day = 60 * 60 * 24
        self.assertEqual(delay, one_day - 10)
