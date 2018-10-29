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
        """Make a mock HTTP request.

        Must be used within a `with .data()` block.
        """
        if self._data is None:
            raise NoMockData()
        return MockResponse(self._data)

    @contextmanager
    def data(self, data: dict):
        """Context manager to provide fake data for a request.

        Usage
        -----
        >>> client = MockTMDBClient()
        >>> with client.data({'id': 1, 'title': 'Walking Dead'}) as data:
        >>>     response = client.search_show(data)
        """
        try:
            self._data = data
            yield data
        finally:
            self._data = None

    def _load_from_disk(self, filename: str) -> dict:
        path = os.path.join(_MOCK_DATA_PATH, filename)
        with open(path, 'r') as f:
            return json.loads(f.read())

    def search_show(self, title: str) -> List[Show]:
        mock = self._load_from_disk('search.json')
        with self.data(mock):
            return super().search_show(title)
