from django.core.mail import send_mail
from users.models import User
from series.models import APIShow


class NotificationBackend:
    """Backend for generic notifications."""

    def notify(self, user: User, tv_show: APIShow):
        pass


class EmailNotifier(NotificationBackend):
    """Notifications with emails."""
    _subject = 'A new episode arrives today !'
    _basic_content = 'Today, a new episode of : '
    _mail_from = 'new_series@uptv.com'

    def notify(self, user: User, tv_show: APIShow):
        send_mail(
            self._subject,
            self.get_full_content(user, tv_show),
            self._mail_from,
            [user.email],
            fail_silently=False,
        )

    def get_full_content(self, user: User, tv_show: APIShow):
        """Create the full content of an email."""
        mail_content = self._basic_content
        # Add show's title to the content
        mail_content += tv_show.title
        return mail_content

    def get_subject(self):
        return self._subject
