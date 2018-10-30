from django.core import mail
from django.test import TestCase

from users.models import User
from series.models import APIShow
from alerts.notifications import EmailNotifier


class EmailTest(TestCase):
    """Email notification testing.
    Inspired from: https://docs.djangoproject.com/en/2.1/topics/testing/tools/#email-services"""

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
