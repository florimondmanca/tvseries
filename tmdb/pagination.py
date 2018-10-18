"""Generic TMDB API pagination utilities."""
from typing import TypeVar, List, Callable

from requests import Response

T = TypeVar('T')


def collect_paginated_results(
        fetch_page: Callable[[int], Response],
        total_pages: Callable[[dict], int],
        extract: Callable[[dict], List[T]]) -> List[T]:
    """Collect all pages of a paginated resource.

    Collection workflow:
    1. Fetch the first page.
    2. Identify the total number of pages from this response.
    3. Fetch the remaining pages, if any.

    :param fetch_page
        A function that takes one argument (the page number) and
        returns a requests.Response object.
    :param total_pages
        A function that takes one argument (the raw JSON data from
        the response) and returns the total number of pages.
    :param extract
        A function that takes one argument (the raw JSON data from
        the response) and returns a list of items of interest.
        For example, this may return the list of full objects in
        a "results" field, or a list of a specific field for each object.
    """
    results: List[T] = []

    response = fetch_page(1)
    data = response.json()
    results.extend(extract(data))

    for page in range(2, total_pages(data) + 1):
        response = fetch_page(page)
        results.extend(extract(response.json()))

    return results
