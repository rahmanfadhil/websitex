# FRONT-END ASSETS
# ------------------------------------------------------------------------------
FROM node:16.17.1-alpine AS frontend

# Create app directory
WORKDIR /code/frontend

# Install app dependencies
COPY ./frontend/package*.json .
RUN npm install

# Copy source files
COPY ./backend /code/backend
COPY ./frontend /code/frontend

# Build frontend and watch for changes
CMD [ "npm", "run", "dev" ]

# Build the production JS and CSS
FROM frontend AS frontend-builder
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
COPY ./backend/requirements /tmp/requirements
RUN pip install -r /tmp/requirements/dev.txt
ENV DJANGO_SETTINGS_MODULE config.settings.development
WORKDIR /code
COPY ./backend .
CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]

FROM base
COPY ./backend/requirements /tmp/requirements
RUN pip install -r /tmp/requirements/prod.txt
ENV DJANGO_SETTINGS_MODULE config.settings.production
WORKDIR /code
COPY ./backend .
COPY --from=frontend-builder /code/backend/static/dist/ /code/backend/static/dist/
CMD python manage.py collectstatic --no-input \
    && python manage.py migrate \
    && daphne -b 0.0.0.0 -p $PORT config.asgi:application
