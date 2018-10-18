import requests
import json
from .show import Show
from datetime import datetime
import os
from dotenv import load_dotenv
from typing import List

load_dotenv()

TMDB_API_KEY = os.getenv('TMDB_API_KEY')

API_URL = "https://api.themoviedb.org/3/"
language = "en-US"

# to get images url : see https://developers.themoviedb.org/3/getting-started/images
# TODO actually get these from configuration/ API and not hardcode it
ICON_URL = "https://image.tmdb.org/t/p/"
small_size = "w154"
big_size = "w300"

# TODO put this in a class and a whole lot a method for all getters that will also handle existence
def search_show(title: str) -> List[Show]:
    """Searches the title in the API to find corresponding tvshows

    :param title: string
    :return: array of Show
    """
    endpoint = "search/tv"
    # Here I only load the first page of results
    # TODO : add searching to more pages
    url = API_URL + endpoint
    resp = requests.get(url, params={"api_key":  TMDB_API_KEY, "language": language, "query": title, "page": 1})
    shows = []
    resp.raise_for_status()
    content = resp.json()
    for json_show in content["results"]:
        show = Show(id=json_show["id"], title=json_show["name"],
                    small_logo_path=ICON_URL + small_size + json_show["poster_path"])
        shows.append(show)
    return shows


def get_show_details(id: int) -> Show:
    """Searches Api for the details of a show

    :param id: id of the show in the APi
    :return: a Show object
    """
    endpoint = "tv/" + str(id)
    url = API_URL + endpoint
    resp = requests.get(url, params={"api_key": TMDB_API_KEY, "language": language})
    resp.raise_for_status()
    content = resp.json()
    title: str = content["name"]
    small_logo: str = ICON_URL + small_size + content["poster_path"]
    big_logo: str = ICON_URL + big_size + content["poster_path"]
    directors: List[str] = [director["name"] for director in content["created_by"]]
    creation_date: datetime = datetime.strptime(content["first_air_date"], "%Y-%m-%d")
    genres: List[str] = [genre["name"] for genre in content["genres"]]
    last_episode_date: datetime = datetime.strptime(content["last_air_date"], "%Y-%m-%d")
    if content["next_episode_to_air"] is not None:
        next_episode_date: datetime = datetime.strptime(content["next_episode_to_air"]["air_date"], "%Y-%m-%d")
    else:
        next_episode_date = None
    synopsis = content["overview"]
    return Show(id=id, title=title, small_logo_path=small_logo, big_logo_path=big_logo,
                synopsis=synopsis, directors=directors, genres=genres, creation_date=creation_date,
                last_episode_date=last_episode_date, next_episode_date=next_episode_date)

