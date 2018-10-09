import requests
import json


api_url = "https://api.themoviedb.org/3/"
api_key = "?api_key=b6f2e2170c53099a5a65cf3d336d242f"
language = "language=en-US"


def search_show(title):
    """
    search title in API

    :param title: string
    :return:
    """
    endpoint = "search/tv"
    url = api_url + endpoint + api_key + "&" + language + "&query=" + title + "&page=1"
    resp = requests.get(url)
    print(resp.status_code)
    if resp.status_code == 200:
        content = json.loads(resp.content)
        print(content)


