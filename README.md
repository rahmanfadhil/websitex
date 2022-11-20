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
$ npm install
```

## Usage

### Run development server

Start additional services for development environment

```
$ docker compose up -d
```

Run migrations

```
$ python manage.py migrate
```

Create a superuser

```
$ python manage.py createsuperuser
```

Run development server

```
$ npm run start
```

Visit http://localhost:8000

### Run tests

Install playwright and its dependencies:

```
$ playwright install
```

Run tests:

```
$ pytest
```
