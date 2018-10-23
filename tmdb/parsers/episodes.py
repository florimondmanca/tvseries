"""Parsers of episode objects."""


from ..datatypes import Episode
from .base import Parser


class EpisodeParser(Parser[Episode]):

    object_class = Episode

    def get_kwargs(self, data: dict) -> dict:
        return {
            'number': data['episode_number'],
            'synopsis': data['overview']
        }
