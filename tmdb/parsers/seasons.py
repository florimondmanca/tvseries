"""Parsers of season objects."""

from typing import List

from tmdb.parsers.episodes import EpisodeParser
from ..datatypes import Season, Episode
from .base import Parser


class SeasonParser(Parser[Season]):

    object_class = Season

    def _get_list_episodes(self, data: dict) -> List[Episode]:
        episodes: List[dict] = data['episodes']
        list_episodes = []
        for episode in episodes:
            episode_parser = EpisodeParser()
            episode = episode_parser.parse(episode)
            list_episodes.append(episode)
        # To be sure that the episodes are sorted in the right order
        list_episodes.sort(key=lambda el: el.number)
        return list_episodes

    def get_kwargs(self, data: dict) -> dict:
        return {
            'number': data['season_number'],
            'episodes': self._get_list_episodes(data)
        }
