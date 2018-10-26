"""Reusable mixin classes."""
from enum import Enum
from typing import Optional


class ImageParserMixin:
    """Mixin class allowing to build the full path to a picture.

    This is motivated by the fact that the TMDB API has a common yet specific
    way of linking to images (TV show picture, episode stills…).
    This mixin can be used by various parser classes to provide this common
    functionality.
    """

    _BASE_URL = 'https://image.tmdb.org/t/p/'
    _PLACEHOLDER_URL_FMT = 'https://via.placeholder.com/{size}'

    class _ImageSize(Enum):
        SMALL = 'w154'
        BIG = 'w300'

    _PLACEHOLDERS = {
        _ImageSize.SMALL: '154x231',
        _ImageSize.BIG: '300x450',
    }

    def get_full_path(self, path: str, size: _ImageSize) -> str:
        """Build a full logo URL from the API poster path and a size code.

        For the documentation about image URLs in the TMDB API, see:
        https://developers.themoviedb.org/3/getting-started/images
        """
        return self._BASE_URL + size.value + path

    def get_placeholder_path(self, size: _ImageSize) -> str:
        """Return a URL to a placeholder image."""
        placeholder_size = self._PLACEHOLDERS[size]
        return self._PLACEHOLDER_URL_FMT.format(size=placeholder_size)

    def get_image_or_placeholder_url(self, path: Optional[str],
                                     size: _ImageSize = None) -> str:
        """Return the full URL to the given image or a placeholder.

        :param path: str, optional
            If None, a URL to a placeholder of the same size will be returned.
        :param size: ImageSize, optional
            Defaults to ImageSize.BIG.
        :return url: str
        """
        if size is None:
            size = ImageSize.BIG
        if path is not None:
            return self.get_full_path(path=path, size=size)
        else:
            return self.get_placeholder_path(size)


# For convenience
ImageSize = ImageParserMixin._ImageSize
