# WebsiteX

A production-ready Django boilerplate.

## Installation

Clone the repo

```
$ git clone https://github.com/rahmanfadhil/websitex.git
$ cd websitex
```

Create a virtual environment

```
$ python3 -m venv venv
$ source venv/bin/activate
```

Install dependencies

```
$ pip install -r requirements.txt
```

## Usage

### Run development server

Start the development server

```
$ docker compose up -d
```

Run migrations

```
$ docker compose exec web python manage.py migrate
```

Create a superuser

```
$ docker compose exec web python manage.py createsuperuser
```

Visit http://localhost:8000

### Run tests

Install playwright and its dependencies:

```
$ docker compose exec web playwright install --with-deps
```

Run tests:

```
$ docker compose exec web python pytest
```
