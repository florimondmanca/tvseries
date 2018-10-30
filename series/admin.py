from django.contrib import admin

from .models import APIShow


@admin.register(APIShow)
class APIShowAdmin(admin.ModelAdmin):
    """Admin panel for API shows."""

    list_display = ('id', 'title', 'first_followed',)
    list_filter = ('first_followed',)
