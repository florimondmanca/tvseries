"""Users administration."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Customized user admin panel."""

    fieldsets = UserAdmin.fieldsets

    # Update the second fieldset (corresponding to personal information)
    # to include the avatar field.
    # See below for default fieldsets:
    # https://github.com/django/django/blob/master/django/contrib/auth/admin.py#L41
    fieldsets[1][1]['fields'] += ('avatar',)

