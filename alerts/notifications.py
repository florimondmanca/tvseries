from django.core.mail import send_mail
from users.models import User
from series.models import APIShow


class NotificationBackend:
    """Backend for generic notifications."""

    def notify(self, user: User, show: APIShow):
        raise NotImplementedError


class EmailNotifier(NotificationBackend):
    """Notifications with emails."""
    _subject = 'A new episode arrives today !'
    _basic_content = 'Today, a new episode of : '
    _mail_from = 'new_series@uptv.com'

    def notify(self, user: User, show: APIShow):
        send_mail(
            self._subject,
            self._get_full_content(show),
            self._mail_from,
            [user.email],
            fail_silently=False,
        )

    def _get_full_content(self, show: APIShow):
        """Create the full content of an email."""
        mail_content = self._basic_content
        mail_content += show.title
        return mail_content

    def get_subject(self):
        return self._subject
