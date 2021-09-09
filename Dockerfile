# FRONT-END ASSETS
# ------------------------------------------------------------------------------
FROM node:16-alpine AS assets

# Create app directory
WORKDIR /code

# Install app dependencies
COPY package*.json ./
RUN npm install

# Bundle app source
COPY ./assets /code/assets
COPY ./rollup.config.mjs .

# Build assets and watch for changes
CMD [ "npm", "run", "dev" ]

# Build the production JS and CSS
FROM assets AS assets-builder
RUN npm run build

# BASE (PYTHON)
# ------------------------------------------------------------------------------

FROM python:3.9-slim-buster AS base

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    # dependencies for building Python packages
    build-essential \
    # psycopg2 dependencies
    libpq-dev \
    # watchdog dependencies
    libyaml-dev \
    # Translations dependencies
    gettext \
    # cleaning up unused files
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

# RELEASES
# ------------------------------------------------------------------------------

FROM base AS development
COPY ./requirements /tmp/requirements
RUN pip install -r /tmp/requirements/dev.txt
ENV DJANGO_SETTINGS_MODULE config.settings.development
WORKDIR /code
COPY . .
CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]

FROM base
COPY ./requirements /tmp/requirements
RUN pip install -r /tmp/requirements/prod.txt
ENV DJANGO_SETTINGS_MODULE config.settings.production
WORKDIR /code
COPY . .
COPY --from=assets-builder /code/static/dist/ /code/static/dist/
RUN DATABASE_NAME="" \
    DATABASE_PORT="" \
    DATABASE_USER="" \
    DATABASE_PASSWORD="" \
    DATABASE_HOST="" \
    MEMCACHED_URL="" \
    BROKER_URL="" \
    AWS_STORAGE_BUCKET_NAME="" \
    python manage.py collectstatic --no-input
CMD [ "gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:80" ]
