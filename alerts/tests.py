from django.core import mail
from django.test import TestCase

from users.models import User
from series.models import APIShow
from alerts.notifications import EmailNotifier


class EmailTest(TestCase):
    """Email notification testing."""

    def test_send_email(self):
        # Add user and tv show
        user = User.objects.create_user(username='username', email='to@example.com', password='password')
        user.save()
        tv_show = APIShow(id='1', title='Test TV Show')
        tv_show.save()
        tv_show.followers.add(user)

        notifier = EmailNotifier()
        notifier.notify(user)

        # Test that one message has been sent.
        self.assertEqual(len(mail.outbox), 1)

        # Verify that the subject of the first message is correct.
        self.assertEqual(mail.outbox[0].subject, notifier.get_subject())

        # Verify that the body of the first message is correct.
        print(mail.outbox[0].body, 'New episodes for these series arrive today : Test TV Show')
