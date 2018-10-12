import requests
import json
from .show import Show
from datetime import datetime


api_url = "https://api.themoviedb.org/3/"
api_key = "?api_key=b6f2e2170c53099a5a65cf3d336d242f"
language = "language=en-US"

icon_url = "https://image.tmdb.org/t/p/"
small_size = "w154"
big_size = "w300/"


def search_show(title: str):
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


def get_show_details(id: int):
    """
    Search Api for the details of a show

    :param id: id of the show in the APi
    :return:
    """
    endpoint = "tv/" + str(id)
    url = api_url + endpoint + api_key + "&" + language
    resp = requests.get(url)
    print(resp.status_code)
    if resp.status_code == 200:
        content = json.loads(resp.content)
        title = content['name']
        small_logo = icon_url + small_size + content["poster_path"]
        big_logo = icon_url + big_size + content["poster_path"]
        directors = [director["name"] for director in content["created_by"]]
        creation_date = datetime.strptime(content["first_air_date"], "%Y-%m-%d")
        genres = [genre["name"] for genre in content["genres"]]
        last_episode_date = datetime.strptime(content["last_air_date"], "%Y-%m-%d")
        if content["next_episode_to_air"]:
            next_episode_date = datetime.strptime(content["next_episode_to_air"]["air_date"], "%Y-%m-%d")
        else:
            next_episode_date = None
        synopsis = content["overview"]
        return Show(id, title=title, small_logo_path=small_logo, big_logo_path=big_logo,
                    synopsis=synopsis, directors=directors, genres=genres, creation_date=creation_date,
                    last_episode_date=last_episode_date, next_episode_date=next_episode_date)

