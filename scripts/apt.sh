#!/usr/bin/env bash

apt-get update

# dependencies for building Python packages
apt-get install -y build-essential

# psycopg2 dependencies
apt-get install -y libpq-dev

# Translations dependencies
apt-get install -y gettext

# cleaning up unused files
apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false
rm -rf /var/lib/apt/lists/*
