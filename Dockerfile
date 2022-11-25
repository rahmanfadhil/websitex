# ASSETS BUILDER
# ------------------------------------------------------------------------------

FROM node:18.12.0-alpine AS assets-builder

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
    # Translations dependencies
    gettext \
    # cleaning up unused files
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

# DEVELOPMENT
# ------------------------------------------------------------------------------

FROM base AS development

# Install python dependencies
COPY ./requirements /tmp/requirements
RUN pip install -r /tmp/requirements/dev.txt

# Install nodejs
RUN apt-get update && apt-get install -y curl
RUN curl -sL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs

# Install nodejs dependencies
WORKDIR /code
COPY ./package*.json ./
RUN npm install

# Use the development django settings
ENV DJANGO_SETTINGS_MODULE config.settings.development

# Copy source code
COPY . .

# Run development server
CMD [ "npm", "run", "start" ]

# PRODUCTION (DEFAULT)
# ------------------------------------------------------------------------------

FROM base

# Install python dependencies
COPY ./requirements /tmp/requirements
RUN pip install -r /tmp/requirements/prod.txt

# Use the production django settings
ENV DJANGO_SETTINGS_MODULE config.settings.production

# Copy source code
WORKDIR /code
COPY . .

# Copy assets static files
COPY --from=assets-builder /code/static/dist/ /code/static/dist/

# Collect all static files
RUN python manage.py collectstatic --no-input

# Run production server
CMD daphne -b 0.0.0.0 -p $PORT config.asgi:application
