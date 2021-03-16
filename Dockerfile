FROM python:3.9-slim-buster

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Install system dependencies
RUN apt-get update \
    # dependencies for building Python packages
    && apt-get install -y build-essential \
    # psycopg2 dependencies
    && apt-get install -y libpq-dev \
    # Translations dependencies
    && apt-get install -y gettext \
    # cleaning up unused files
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY ./requirements /requirements
RUN pip install -r /requirements/dev.txt

# Set work directory
WORKDIR /code

# Set environment variables
ENV DJANGO_SETTINGS_MODULE config.settings.production

# Copy project
COPY . /code/

CMD [ "gunicorn", "config.wsgi:appplication" ]
