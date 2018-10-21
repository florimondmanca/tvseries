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

### Configuring email delivery of alerts

Alerts about new episodes are delivered via email.

In production, email delivery is powered by [SendGrid](https://sendgrid.com). Credentials are associated to the `uptv` Heroku application and not disclosed here, obviously.

It is also possible to use SendGrid in development. You will need to acquire a valid SendGrid API key (free hobby accounts are available) and to provide it through the `SENDGRID_API_KEY` environment variable.

> Note that in `DEBUG` mode, emails will purposefully NOT be sent unless the `SENDGRID_SANDBOX_MODE_IN_DEBUG` is set to `False`. For more information, see [django-sendgrid-v5](https://github.com/sklarsa/django-sendgrid-v5).

If SendGrid email is not configured, emails will not be sent but alerts will still be logged to the console.

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
