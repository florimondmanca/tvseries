"""Series models."""
from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
from tmdb.shortcuts import retrieve_show

User = get_user_model()


class APIShowManager(models.Manager):
    """Custom manager for APIShow objects."""

    def create_from_api(self, show_id: int) -> 'APIShow':
        """Create and store a new APIShow from its ID on the TMDB API."""
        show = retrieve_show(show_id)
        return self.create(id=show.id,
                           title=show.title,
                           description=show.synopsis)

    def follows(self, show_id: int, user: User) -> bool:
        """Return whether a user follows a show given by ID.

        :param user : User
            A user object, which may or may not be authenticated.
        :param show_id : int
            The unique identifier for the show,
            (which might not be in database yet.)
        :return follows : bool
        """
        if user.is_authenticated:
            qs = self.get_queryset()
            return qs.filter(pk=show_id, followers__id=user.pk).exists()
        return False


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
    followers: models.Manager = models.ManyToManyField(
        to=User, related_name='favorites', blank=True,
        help_text='Users that will receive alerts about this show.',
    )

    def is_followed_by(self, user: User) -> bool:
        """Return whether a user follows this show.

        :param user : User
            A user object, which may or may not be authenticated.
        :return follows : bool
        """
        if user.is_authenticated:
            return self.followers.filter(id=user.pk).exists()
        return False

    @property
    def num_followers(self) -> int:
        """Get the number of users following this show."""
        return self.followers.count()

    def __str__(self) -> str:
        """Represent a show by its API ID."""
        return str(self.id)
