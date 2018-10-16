from django.db import models

# Create your models here.


class APIShow(models.Model):
    """Represents a show retrievable through the TMDB API."""

    id = models.PositiveIntegerField(
        primary_key=True,
        help_text="The show's ID on the TMDB API.",
    )
    title = models.CharField(
        max_length=100, null=True,
        help_text="The show's name on the TMDB API.",
    )
    description = models.TextField(
        null=True,
        help_text="The show's overview on the TMDB API.",
    )

    def __str__(self) -> str:
        return f'Show<{self.id}: {self.title}>'
