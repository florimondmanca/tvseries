from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    avatar = models.ImageField()
    # followed_series = models.ManyToManyField(Content)
    def __str__(self):
        return self.last_name + " " + self.first_name