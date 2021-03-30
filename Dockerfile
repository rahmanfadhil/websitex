FROM node:14-alpine AS builder

# Create app directory
WORKDIR /code

# Install app dependencies
COPY package*.json ./
RUN npm install

# Bundle app source
COPY ./assets /code/assets
COPY ./webpack.config.js .

# Build the production JS and CSS
RUN npm run build

FROM python:3.9-slim-buster

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV DJANGO_SETTINGS_MODULE config.settings.production

# Install system dependencies
COPY ./scripts/apt.sh /apt.sh
RUN /apt.sh

# Install Python dependencies
COPY ./requirements /requirements
RUN pip install -r /requirements/prod.txt

# Set work directory
WORKDIR /code

# Copy project
COPY . /code/

# Copy bundled JS and CSS
COPY --from=builder /code/static/dist/ /code/static/dist/

CMD [ "/code/scripts/entrypoint.sh" ]
