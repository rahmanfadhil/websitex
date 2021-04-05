#!/usr/bin/env bash

apt-get update

# dependencies for building Python packages
apt-get install -y build-essential

# psycopg2 dependencies
apt-get install -y libpq-dev

# watchdog dependencies
apt-get install -y libyaml-dev

# python-magic dependencies
apt-get install -y libmagic1

# Translations dependencies
apt-get install -y gettext

# cleaning up unused files
apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false
rm -rf /var/lib/apt/lists/*
