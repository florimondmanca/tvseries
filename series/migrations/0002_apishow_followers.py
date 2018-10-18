# Generated by Django 2.1.2 on 2018-10-17 10:42

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('series', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='apishow',
            name='followers',
            field=models.ManyToManyField(blank=True, help_text='Users that will receive alerts about this show.', related_name='favorites', to=settings.AUTH_USER_MODEL),
        ),
    ]