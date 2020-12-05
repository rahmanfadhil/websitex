# DjangoX

A highly-customized version of [DjangoX](https://github.com/wsvincent/djangox), a batteries-included Django boilerplate.

## Features

- Django 3.1
- Bootstrap 4.5
- Gulp, Sass, and Rollup
- PostgreSQL

**Other Dependencies**

- django-debug-toolbar
- django-allauth
- django-environ
- whitenoise
- gunicorn

## Prerequisite

- Python (3.8 or later)
- Node.js (any LTS version)

## Instalation

Create a new virtual environment.

```
$ python -m venv venv
```

Activate the virtual environment, and install the Python dependencies.

```
$ source venv/bin/activate
$ pip install -r requirements.txt
```

Install Node.js dependencies (required to build the front-end assets).

```
$ npm install
```

## Development

To run the development server, you can simply run `npm start`. This will run the Django development server and build the front-end assets. It will automatically rebuild the assets if changed.

```
$ npm start
```

If you just want to run the Django server, you can run:

```
$ python manage.py runserver
```

Or, if you just want to build the front-end assets, you can run:

```
$ npm run build
```
