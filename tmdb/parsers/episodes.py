"""Parsers of episode objects."""
from datetime import datetime, date

from tmdb.parsers.mixins import ImageMixin
from ..datatypes import Episode
from .base import Parser


class EpisodeParser(ImageMixin, Parser[Episode]):
    """Parser of Episode objects."""

    object_class = Episode
    _STILL_SIZE = 'w300'
    _PLACEHOLDER_URL = 'https://via.placeholder.com/300x170'

    def _get_still_path(self, data: dict) -> str:
        poster_path = data['still_path']
        if poster_path is not None:
            return self.get_full_path(
                path=poster_path,
                size_code=self._STILL_SIZE,
            )
        else:
            return self._PLACEHOLDER_URL

    def _get_air_date(self, data: dict) -> date:
        return datetime.strptime(data['air_date'], '%Y-%m-%d').date()

    def get_kwargs(self, data: dict) -> dict:
        return {
            'number': data['episode_number'],
            'synopsis': data['overview'],
            'still_path': self._get_still_path(data),
            'air_date': self._get_air_date(data),
        }
