#!/bin/bash

echo "Applying database migrations..."
python manage.py makemigrations
python manage.py migrate

echo "Starting Django app..."
exec python manage.py runserver 0.0.0.0:8000
