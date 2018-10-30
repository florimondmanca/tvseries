from django.contrib import admin, messages

from alerts.notifications import EmailNotifier
from .models import APIShow


@admin.register(APIShow)
class APIShowAdmin(admin.ModelAdmin):
    """Admin panel for API shows."""

    list_display = ('id', 'title', 'first_followed',)
    list_filter = ('first_followed',)
    actions = ['email_followers']

    def email_followers(self, request, queryset):
        notifier = EmailNotifier()
        num_emails = 0
        for show in queryset:
            for user in show.followers.all():
                notifier.notify(user, show)
            num_emails += show.followers.count()
        messages.success(request, f'Successfully sent {num_emails} alerts')

    email_followers.short_description = "Email followers of selected shows"
