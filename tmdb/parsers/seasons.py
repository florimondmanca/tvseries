"""Parsers of season objects."""

from typing import List

from ..datatypes import Season, Episode
from .base import Parser


class SeasonParser(Parser[Season]):

    object_class = Season

    @staticmethod
    def _parse_episode(episode: dict) -> Episode:
        number: int = episode['episode_number']
        synopsis: str = episode['overview']
        return Episode(number=number, synopsis=synopsis)

    def _get_list_episodes(self, data: dict) -> List[Episode]:
        episodes: List[dict] = data['episodes']
        list_episodes = []
        for episode in episodes:
            list_episodes.append(self._parse_episode(episode))
        # To be sure that the episodes are sorted in the right order
        list_episodes.sort(key=lambda el: el.number)
        return list_episodes

    def get_kwargs(self, data: dict) -> dict:
        return {
            'number': data['season_number'],
            'list_episodes': self._get_list_episodes(data)
        }