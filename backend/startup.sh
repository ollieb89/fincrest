#!/bin/bash
echo "🔹 Starting Django Backend on Azure..."

# Navigate to backend directory
cd backend

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Install dependencies
pip install -r requirements.txt

# Run Migrations
python manage.py migrate --noinput

# Collect Static Files
python manage.py collectstatic --noinput

# Start Gunicorn
gunicorn --bind=0.0.0.0 --timeout 600 fincrest.wsgi:application
