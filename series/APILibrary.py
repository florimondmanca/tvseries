import requests
import json
from .show import Show


api_url = "https://api.themoviedb.org/3/"
api_key = "?api_key=b6f2e2170c53099a5a65cf3d336d242f"
language = "language=en-US"

icon_url = "https://image.tmdb.org/t/p/"
small_size = "w154"
big_size = "w300/"


def search_show(title):
    """
    search title in API

    :param title: string
    :return: array of Show
    """
    endpoint = "search/tv"
    url = api_url + endpoint + api_key + "&" + language + "&query=" + title + "&page=1"
    resp = requests.get(url)
    print(resp.status_code)
    shows = []
    if resp.status_code == 200:
        content = json.loads(resp.content)
        for json_show in content["results"] :
            show = Show(json_show["id"], json_show["name"], icon_url + small_size + json_show["poster_path"])
            shows.append(show)
    return shows


