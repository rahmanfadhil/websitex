# DjangoX

A production-ready Django boilerplate based on [DjangoX](https://github.com/wsvincent/djangox).

## Features

- Django 3.1
- Bootstrap 5
- PostgreSQL
- SSL (in production).

**Other Dependencies**

- [django-crispy-forms](https://github.com/django-crispy-forms/django-crispy-forms) to easily build forms.
- [django-debug-toolbar](https://django-debug-toolbar.readthedocs.io/en/latest/) to debug the app.
- [django-allauth](https://django-allauth.readthedocs.io/en/latest/installation.html) to work with authentication.
- [django-environ](https://django-environ.readthedocs.io/en/latest/) to collect Django settings from environment variables.
- [whitenoise](http://whitenoise.evans.io/en/stable/index.html) to serve static files in production.
- [gunicorn](https://gunicorn.org/) to run server in production environment.
- [psycopg2](https://www.psycopg.org/docs/) to work with PostgreSQL.

## Installation

Create a new virtual environment.

```
$ python -m venv venv
```

Activate the virtual environment, and install the Python dependencies.

```
$ source venv/bin/activate
$ pip install -r requirements.txt
```

## Development

To run the development server, you can simply execute the `runserver` Django command just like any other django projects.

```
$ python manage.py runserver
```

To run the production server, you need to setup the environment variables first, then run gunicorn.

```
$ export DEBUG=False
$ gunicorn -b 0.0.0.0:8000 config.wsgi:application
```
