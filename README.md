# My Django Site

[![CI](https://github.com/jinxbuilds/my-django-site/actions/workflows/ci.yml/badge.svg)](https://github.com/jinxbuilds/my-django-site/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Django](https://img.shields.io/badge/django-5.2%20LTS-0c4b33)

A small blog built with Django. Posts are written in the Django admin and shown on a public,
paginated list with individual post pages. Drafts and posts scheduled for the future stay hidden
until their publish date.

## Features

- Public post list (paginated) and post detail pages
- Draft and scheduled publishing via `published_date`
- Admin with search, filters and a bulk "Publish now" action
- Environment-based configuration, production security settings
- Test suite, linting (Ruff), pre-commit hooks and GitHub Actions CI

## Tech stack

Python 3.10+ · Django 5.2 LTS · SQLite (development) · Ruff

## Getting started

```bash
git clone https://github.com/jinxbuilds/my-django-site.git
cd my-django-site

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -r requirements-dev.txt
cp .env.example .env             # then edit values

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000 for the blog and http://127.0.0.1:8000/admin/ to write posts.

## Configuration

Settings are read from environment variables, or from a `.env` file in the project root.

| Variable | Default | Description |
|---|---|---|
| `DJANGO_SECRET_KEY` | — | Required when `DJANGO_DEBUG` is off. |
| `DJANGO_DEBUG` | `False` | Set `True` for local development only. |
| `DJANGO_ALLOWED_HOSTS` | `localhost,127.0.0.1` | Comma-separated host names. |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | empty | Comma-separated origins, e.g. `https://example.com`. |
| `DJANGO_TIME_ZONE` | `Asia/Kolkata` | Any IANA time zone name. |
| `DJANGO_SECURE_SSL_REDIRECT` | `True` | Redirect HTTP to HTTPS when `DEBUG` is off. |
| `DJANGO_SECURE_HSTS_SECONDS` | `3600` | HSTS max-age when `DEBUG` is off. |

Generate a secret key with:

```bash
python -c "from django.core.management.utils import get_random_secret_key as k; print(k())"
```

## Development

```bash
python manage.py test            # run the test suite
ruff check . && ruff format .    # lint and format
pre-commit install               # run checks automatically on every commit
pip-audit -r requirements.txt    # check dependencies for known vulnerabilities
```

## Project structure

```
.
├── blog/                 # Blog app: models, views, admin, templates, tests
├── mysite/               # Project settings, URLs, WSGI/ASGI
├── static/css/           # Site stylesheet
├── templates/base.html   # Shared page layout
├── .env.example          # Template for local configuration
└── .github/workflows/    # CI pipeline
```

## Deployment

1. Set `DJANGO_DEBUG=False`, a fresh `DJANGO_SECRET_KEY` and your domain in
   `DJANGO_ALLOWED_HOSTS` (and `DJANGO_CSRF_TRUSTED_ORIGINS`).
2. `pip install -r requirements.txt`
3. `python manage.py migrate`
4. `python manage.py collectstatic` and serve `staticfiles/` at `/static/`.
5. Run `python manage.py check --deploy` and fix anything it reports.

On PythonAnywhere, add the env vars to your WSGI file or a `.env` next to `manage.py`, and map
`/static/` to the `staticfiles/` directory on the Web tab.
