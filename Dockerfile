# FRONTEND BUILDER
# ------------------------------------------------------------------------------
FROM node:18.12.0-alpine AS frontend-builder

WORKDIR /code
COPY ./package*.json ./
RUN npm install
COPY . .
RUN npm run build

# BASE (PYTHON)
# ------------------------------------------------------------------------------

FROM python:3.10.7-slim-bullseye AS base

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    # dependencies for building Python packages
    build-essential \
    # psycopg2 dependencies
    libpq-dev \
    # Translations dependencies
    gettext \
    # cleaning up unused files
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

# BASE IMAGE (PYTHON) WITH NODE.JS
# ------------------------------------------------------------------------------

FROM base AS with-nodejs

# Install curl
RUN apt-get update && apt-get install -y curl

# Install nodejs
RUN curl -sL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs

# RELEASES
# ------------------------------------------------------------------------------

FROM with-nodejs AS development
COPY ./requirements /tmp/requirements
RUN pip install -r /tmp/requirements/dev.txt
ENV DJANGO_SETTINGS_MODULE config.settings.development
WORKDIR /code
COPY ./package*.json ./
RUN npm install
COPY . .
CMD [ "npm", "run", "start" ]

FROM base
COPY ./requirements /tmp/requirements
RUN pip install -r /tmp/requirements/prod.txt
ENV DJANGO_SETTINGS_MODULE config.settings.production
WORKDIR /code
COPY . .
COPY --from=frontend-builder /code/static/dist/ /code/static/dist/
CMD python manage.py collectstatic --no-input \
    && python manage.py migrate \
    && daphne -b 0.0.0.0 -p $PORT config.asgi:application
