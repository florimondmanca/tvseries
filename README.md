# UpTV

[![Build Status](https://img.shields.io/travis-ci/florimondmanca/uptv.svg?style=flat-square)](https://travis-ci.org/florimondmanca/uptv)
[![Python](https://img.shields.io/badge/python-3.7-blue.svg?style=flat-square)](https://docs.python.org/3/)
[![Django](https://img.shields.io/badge/django-2.1-blue.svg?style=flat-square)](https://www.djangoproject.com)
[![API](https://img.shields.io/badge/api_provider-tmdb-orange.svg?style=flat-square)](https://www.themoviedb.org/documentation/api)

Never miss on your favorite TV show's new episodes! :boom:

## Production
The application is available on https://uptv.herokuapp.com/. Sign up to start subscribing to TV shows and getting notifications for the latest episodes!

## Install

Create a `.env` file at the project root with your credentials (for details, see [Settings](#settings)):

```dotenv
TMDB_API_KEY=...
SENGRID_API_KEY=...
```

Depending on how you want to run UpTV, some extra steps may be necessary — see below.

## Quickstart

### Using Docker

This project requires Python 3.7+. If you don't have it installed on your machine, we provide a Docker Compose setup. You will need [Docker](https://docs.docker.com/install/) and [Docker Compose](https://docs.docker.com/compose/) installed.

The Docker Compose setup runs UpTV in production mode: hot-reloading is disabled, a PostgreSQL database is used instead of SQLite, and the alerts worker will start.

To run UpTV using Docker, run:

```bash
docker-compose up -d
```

The app will be available at http://localhost:8000.

### Using local Python 3.7+

If you have Python 3.7+, you can run UpTV without Docker. However, a few more installation steps are required:

```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
python manage.py migrate
```

You can now start the development server:

```bash
python manage.py runserver
```

The app will be available at http://localhost:8000.

By default, the alerts worker won't start in development. To activate it, use:

```bash
export ALERTS_ACTIVE=1  # or set it in .env
python manage.py runserver --noreload
```

> **Note** : using this method, the alerts worker will run in sandbox mode and emails won't be delivered. To force email delivery, use the `ALERTS_FORCE_EMAIL` setting (see below).

To use the Gunicorn production server instead, use:

```bash
gunicorn uptv.wsgi -c uptv.gunicorn
```

## Settings

The following settings are available and can be defined in your `.env` file:

- `TMDB_API_KEY` (no default): used to query the TheMovieDatabase (TMDB) API, which provides our data. If you don't have an API key, you can create a (free) TMDB account. Refer to the [Getting Started guide](https://developers.themoviedb.org/3/getting-started/introduction).
- `SENDGRID_API_KEY` (no default): used to send alerts via email using SendGrid. For details, see [django-sendgrid-v5](https://github.com/sklarsa/django-sendgrid-v5). 
- `ALERTS_ACTIVE` (default: `False`): whether to start the alerts worker upon server startup.
- `ALERTS_FORCE_EMAIL` (default: `False`): whether to force the alerts worker to deliver emails in development. If `False`, emails will not be delivered (useful for local testing). This setting has no effect in production mode.

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
