"""TMDB mocks."""
import json
import os
from contextlib import contextmanager
from typing import List

import requests

from tmdb.client import TMDBClient
from tmdb.datatypes import Show

_HERE = os.path.dirname(os.path.abspath(__file__))
_MOCK_DATA_PATH = os.path.join(_HERE, 'mock_data')


class NoMockData(Exception):
    """Raised when trying to make a mock request with having set mock data."""


class MockResponse(requests.Response):
    """Mock of a GET 200 OK response with JSON data."""

    def __init__(self, data: dict):
        super().__init__()
        self._data = data
        self.status_code = 200

    def json(self) -> dict:
        return self._data


class MockTMDBClient(TMDBClient):
    """Mock of the TMDB API client for usage in testing."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._data = None

    def _make_request(self, url: str, params: dict):
        """Override the default implementation to make a mock HTTP request.

        Must be used within a `with .data()` block.
        """
        if self._data is None:
            raise NoMockData()
        return MockResponse(self._data)

    def search_show(self, title: str) -> List[Show]:
        with self.data('search.json'):
            return super().search_show(title)

    @contextmanager
    def data(self, from_file: str = None, data: dict = None):
        """Context manager to provide fake JSON data for a request.

        :param from_file : str
            Used to load data from a file, only if `data` is not passed.
        :param data : dict
            JSON data to be attached to the request.

        Usage
        -----
        >>> client = MockTMDBClient()
        >>> with client.data(from_file='search.json') as data:
        >>>     response = client.search_show(data)
        """
        if data is None:
            data = self._load_from_disk(from_file)
        try:
            self._data = data
            yield data
        finally:
            self._data = None

    def _load_from_disk(self, filename: str) -> dict:
        path = os.path.join(_MOCK_DATA_PATH, filename)
        with open(path, 'r') as f:
            return json.loads(f.read())
