#!/usr/bin/env bash
# Exit on error
set -o errexit

pipenv install --deploy --system
python manage.py collectstatic --no-input
python manage.py migrate