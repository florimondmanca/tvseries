from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from series.models import APIShow
from users.models import User
from . import settings


class NotificationBackend:
    """Backend for generic notifications."""

    def notify(self, user: User, show: APIShow):
        raise NotImplementedError


class EmailNotifier(NotificationBackend):
    """Notifications with emails."""

    def get_subject(self, show: APIShow) -> str:
        return f'{show.title}: new episodes airing today'

    @property
    def mail_from(self) -> str:
        return settings.MAIL_FROM

    def get_html_message(self, user: User, show: APIShow) -> str:
        """Return the HTML contents of an email alert."""
        context = {
            'user': user,
            'show': show,
        }
        return render_to_string('alerts/alert.html', context=context)

    def notify(self, user: User, show: APIShow):
        html = self.get_html_message(user, show)
        message = strip_tags(html)
        send_mail(
            subject=self.get_subject(show),
            message=message,
            html_message=html,
            from_email=self.mail_from,
            recipient_list=[user.email],
            fail_silently=False,
        )
