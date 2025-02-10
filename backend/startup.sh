#!/bin/bash

# Activate virtual environment
source /home/site/wwwroot/backend/antenv/bin/activate

# Run Django Migrations
echo "Running Django Migrations..."
python /home/site/wwwroot/backend/fincrest/manage.py migrate --noinput

# Collect Static Files
echo "Collecting static files..."
python /home/site/wwwroot/backend/fincrest/manage.py collectstatic --noinput

# Start Gunicorn server
echo "Starting Gunicorn..."
exec gunicorn --workers=4 --timeout 600 --bind=0.0.0.0:8000 fincrest.wsgi:application
