from django.core.mail import send_mail
from users.models import User

class NotificationBackend:
    def notify(self, user:User):
        pass


class EmailNotifier(NotificationBackend):
    _subject = 'Your favourite series arrive today !'
    _content = 'New episodes for these series arrive today : '
    _mail_from = 'new_series@uptv.com'

    def notify(self, user: User):
        send_mail(
            self._subject,
            self.get_full_content(user),
            self._mail_from,
            [user.email],
            fail_silently=False,
        )

    def get_full_content(self, user: User):
        mail_content = self._content
        for followed_show in user.favorites.all():
            mail_content += followed_show.title + "\n"
        return mail_content