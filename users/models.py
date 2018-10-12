"""Users models."""
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user.

    This inherits all the fields from Django's basic user,
    but also has an avatar.
    """
    avatar = models.ImageField(null=True, blank=True)

    def __str__(self) -> str:
        """Represent the user by their full name."""
        return self.get_full_name()
