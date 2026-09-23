#!/usr/bin/env bash
# Exit on error
set -o errexit

# install pipenv globally in the build container
pip install pipenv

# install dependencies using pipenv
pipenv install --deploy --system

# collect static files and run migrations
python manage.py collectstatic --no-input
python manage.py migrate