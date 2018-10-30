"""TMDB client shortcut functions."""

from typing import List

from tmdb.client import tmdb_client
from tmdb.datatypes import Show, Season


def search_shows(title: str) -> List[Show]:
    """Search shows by title in the TMDB API.

    :param title: str
    :return shows: list of Show
    """
    return tmdb_client.search_show(title)


def retrieve_show(show_id: int) -> Show:
    """Retrieve a show on the TMDB API.

    :param show_id: int
        ID of the show in the TMDB API.
    :return: Show
    """
    return tmdb_client.retrieve_show(show_id)


def retrieve_season(show_id: int, number: int) -> Season:
    """Retrieve a given season for a show.

    :param show_id: int
        ID of the show in the TMDB API.
    :param number:
        Number of the reason.
        Not checked to be within the range of existing season.
    :return season: Season
    """
    return tmdb_client.retrieve_season(show_id, number)
