# UpTV

[![Build Status](https://img.shields.io/travis-ci/florimondmanca/uptv.svg?style=flat-square)](https://travis-ci.org/florimondmanca/uptv)
[![Python](https://img.shields.io/badge/python-3.7-blue.svg?style=flat-square)](https://docs.python.org/3/)
[![Django](https://img.shields.io/badge/django-2.1-blue.svg?style=flat-square)](https://www.djangoproject.com)
[![API](https://img.shields.io/badge/api_provider-tmdb-orange.svg?style=flat-square)](https://www.themoviedb.org/documentation/api)

Never miss on your favorite TV series new episodes! :boom:

## Install

Install dependencies:

```
$ python3 -m venv env
$ source env/bin/activate
$ pip install -r requirements.txt
```

## Quickstart

Start development server:

```
$ python manage.py runserver
```

### Settings

The following settings are available and can be defined in a git-ignored `.env` file located at the root of your project directory:

- `TMDB_API_KEY`: will be used to retrieve and search TV shows on the TheMovieDatabase (TMDB) API. Acquiring an API key requires to create a (free) TMDB account. Please refer to the API's [Getting Started guide](https://developers.themoviedb.org/3/getting-started/introduction) for how to create an API key.

## Contributing

- Create a branch, e.g. `feature/awesome-feature` or `fix/very-nasty-bug`.
- Add commits.
- When ready, push to remote: `git push -u origin feature/awesome-feature`.
- [Open a Pull Request](https://github.com/florimondmanca/uptv/compare): document the changes and provide any useful additional context.
- Ask someone to review your code. 🔎🤝
- When ready and tests pass: merge it!

### Conventions

These are conventions we recommend to apply throughout the project. They are being updated as we agree upon new conventions.

#### View names

Use underscore-separated view names: `search_series` instead of `search-series`.
