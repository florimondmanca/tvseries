from django.contrib import admin

from .models import APIShow
from alerts.jobs import AiringShowsJob


@admin.register(APIShow)
class APIShowAdmin(admin.ModelAdmin):
    """Admin panel for API shows."""

    list_display = ('id', 'title', 'first_followed',)
    list_filter = ('first_followed',)
    actions = ['email_followers']

    def email_followers(self, request, queryset):
        notifier = AiringShowsJob()
        for show in queryset:
            notifier.notify_followers(show)

    email_followers.short_description = "Email followers of selected shows"
