"""Reusable mixin classes."""


class ImageMixin:
    """Mixin class allowing to build the full path to a picture.

    This is motivated by the fact that the TMDB API has a common yet specific
    way of linking to images (TV show picture, episode stills…).
    This mixin can be used by various parser classes to provide this common
    functionality.
    """

    BASE_URL = 'https://image.tmdb.org/t/p/'

    def get_full_path(self, path: str, size_code: str) -> str:
        return self.BASE_URL + size_code + path
