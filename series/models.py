"""Series models."""
from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
from series.APILibrary import get_show_details

User = get_user_model()


class APIShowManager(models.Manager):

    def create_from_api(self, show_id: int) -> 'APIShow':
        show = get_show_details(show_id)
        return self.create(id=show.id,
                           title=show.title,
                           description=show.synopsis)


class APIShow(models.Model):
    """Represents a show retrievable through the TMDB API.

    A show is followed by zero, one or more users.
    A user can follow (i.e. mark as favorite) zero, one or more shows.

    Usage
    -----
    Access a show's followers:
    >>> show = APIShow.objects.first()
    >>> show.followers.all()
    <QuerySet []>

    Access a user's favorite shows:
    >>> user = User.objects.first()
    >>> user.favorites.all()
    <QuerySet []>
    """

    objects = APIShowManager()

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
    first_followed = models.DateTimeField(
        auto_now_add=True,
        help_text='When the show was first followed.',
    )
    followers = models.ManyToManyField(
        to=User, related_name='favorites', blank=True,
        help_text='Users that will receive alerts about this show.',
    )

    def __str__(self) -> str:
        """Represent a show by its API ID."""
        return str(self.id)
