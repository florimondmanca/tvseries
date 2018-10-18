# Generated by Django 2.1.2 on 2018-10-17 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='APIShow',
            fields=[
                ('id', models.PositiveIntegerField(help_text="The show's ID on the TMDB API.", primary_key=True, serialize=False)),
                ('title', models.CharField(help_text="The show's name on the TMDB API.", max_length=100, null=True)),
                ('description', models.TextField(help_text="The show's overview on the TMDB API.", null=True)),
                ('first_followed', models.DateTimeField(auto_now_add=True, help_text='When the show was first followed.')),
            ],
        ),
    ]
