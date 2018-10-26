"""Parsers of season objects."""

from typing import List

from tmdb.parsers.episodes import EpisodeParser
from ..datatypes import Season, Episode
from .base import Parser


class SeasonParser(Parser[Season]):

    object_class = Season

    def _get_episodes(self, data: dict) -> List[Episode]:
        episodes: List[dict] = data['episodes']
        episode_parser = EpisodeParser()
        list_episodes = [episode_parser.parse(episode) for episode in episodes]
        # To be sure that the episodes are sorted in the right order
        list_episodes.sort(key=lambda el: el.number)
        return list_episodes

    def get_kwargs(self, data: dict) -> dict:
        return {
            'number': data['season_number'],
            'episodes': self._get_episodes(data)
        }
