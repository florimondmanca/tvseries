from django.contrib import admin
from .models import APIShow


@admin.register(APIShow)
class APIShowAdmin(admin.ModelAdmin):
    """Admin panel for API shows."""
