"""TMDB API client.

Note
----
For looser coupling, external packages should probably use the
shortcut functions defined in shortcuts.py.
"""

import os
import warnings
from datetime import datetime
from typing import List, Union, Type

import requests

from .datatypes import Show


class ShowParser:
    """Convert raw show API data to actual Show objects."""

    ICON_URL = 'https://image.tmdb.org/t/p/'
    SMALL_SIZE = 'w154'
    BIG_SIZE = 'w300'

    def for_list(self, data: dict) -> Show:
        """Build a Show object suited for displaying in lists.

        :param data: dict
            Dictionary containing raw API data about the show.
        :return show: Show
        """
        return Show(**self._get_common_kwargs(data))

    def for_detail(self, data: dict) -> Show:
        """Build a Show object with all its details.

        :param data: dict
            Dictionary containing raw API data about the show.
        :return show: Show
        """
        return Show(
            **self._get_common_kwargs(data),
            synopsis=data['overview'],
            big_logo_path=self._get_big_logo_path(data['poster_path']),
            genres=[genre['name'] for genre in data['genres']],
            directors=[director['name'] for director in data['created_by']],
            creation_date=self._parse_date(data['first_air_date']),
            last_episode_date=self._parse_date(data['last_air_date']),
            next_episode_date=self._parse_date(data['next_episode_to_air']),
        )

    def _get_common_kwargs(self, data: dict) -> dict:
        """Return Show arguments common to list and detail parsers."""
        return {
            'id': data['id'],
            'title': data['name'],
            'small_logo_path': self._get_small_logo_path(data['poster_path']),
        }

    @staticmethod
    def _parse_date(date: Union[str, None]) -> datetime.date:
        """Parse a date (which might be null) as returned by the API."""
        if date is None:
            return None
        return datetime.strptime(date, '%Y-%m-%D')

    def _get_logo_path(self, poster_path: Union[str, None],
                       size_code: str) -> Union[str, None]:
        """Build a full logo URL from the API poster path and a size code.

        For the documentation about image URLs in the TMDB API, see:
        https://developers.themoviedb.org/3/getting-started/images
        """
        if poster_path is not None:
            return self.ICON_URL + size_code + poster_path
        else:
            return None

    def _get_small_logo_path(self, poster_path):
        return self._get_logo_path(poster_path, size_code=self.SMALL_SIZE)

    def _get_big_logo_path(self, poster_path):
        return self._get_logo_path(poster_path, size_code=self.BIG_SIZE)


class TMDBClient:
    """Client for interacting with the TMDB API."""

    LANGUAGE = 'en-US'
    ROOT_URL = 'https://api.themoviedb.org/3'

    show_parser_class: Type[ShowParser] = ShowParser

    def __init__(self, api_key: str):
        self.api_key = api_key

    def _build_url(self, endpoint: str) -> str:
        """Build the full URL from an endpoint.

        Example:
        _build_url('search/tv') -> 'https://api.themoviedb.org/3/search/tv'
        """
        parts = (self.ROOT_URL, endpoint)
        return '/'.join(part.strip('/') for part in parts)

    def _request(self, endpoint: str, params: dict = None,
                 raise_for_status: bool = True) -> requests.Response:
        """Perform a request to the API.

        :param endpoint: str
        :param params: dict
            GET parameters passed to the underlying call to `requests.get()`.
        :param raise_for_status: bool, optional
            If True (the default), an exception is raised if the response
            has an error status code (400 or greater).
            See Requests' full documentation on status codes:
            http://docs.python-requests.org/en/master/user/quickstart/#response-status-codes
        :returns response
        """
        if params is None:
            params = {}

        # Attach the API key and language if not given
        params.setdefault('api_key', self.api_key)
        params.setdefault('language', self.LANGUAGE)

        url = self._build_url(endpoint)
        resp = requests.get(url, params=params)

        if raise_for_status:
            resp.raise_for_status()

        return resp

    def _get_show_parser(self) -> ShowParser:
        return self.show_parser_class()

    def search_show(self, title: str) -> List[Show]:
        """Search the title in the API to find corresponding TV shows.

        Note: only the first page of results is returned; support for
        pagination could be added in the future.

        :param title: string
        :return: list of Show objects
        """
        resp = self._request('search/tv', {
            'query': title,
            'page': 1,
        })
        content: dict = resp.json()
        parser = self._get_show_parser()
        shows = [parser.for_list(result) for result in content['results']]
        return shows

    def retrieve_show(self, show_id: int) -> Show:
        """Retrieve details of a show.

        :param show_id: id of the show in the API.
        :return: a Show object
        """
        resp = self._request(f'tv/{show_id}')
        data: dict = resp.json()
        parser = self._get_show_parser()
        return parser.for_detail(data)


def get_tmdb_client(api_key: str = None) -> TMDBClient:
    """Build and return a TMDB client.

    :param api_key: str, optional
        If not given, the API key is retrieved from the TMDB_API_KEY
        environment variable.
        If the environment variable is not set, raises a warning.
    :return client: TMDBClient
    :raises UserWarning:
        If the TMDB_API_KEY environment variable is not set,
        but it was used to build the client.
    """
    if api_key is None:
        api_key = os.getenv('TMDB_API_KEY')
        if api_key is None:
            message = (
                'TMDB_API_KEY environment variable not set! Requests to '
                'the TMDB API will most likely fail.'
            )
            warnings.warn(message)
    return TMDBClient(api_key=api_key)


# Provide a default global TMDB client for convenience
tmdb_client = get_tmdb_client()
