#!/bin/sh

echo "Starting application setup..."

# Apply database migrations (including background_task migrations)
echo "Applying database migrations..."
python manage.py makemigrations
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput

# Create superuser if DJANGO_SUPERUSER_USERNAME is set and the user does not already exist
if [ "$DJANGO_SUPERUSER_USERNAME" ]; then
  echo "Checking if superuser exists..."
  if ! python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); exit(User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists())"; then
    echo "Creating superuser..."
    python manage.py createsuperuser --noinput --username $DJANGO_SUPERUSER_USERNAME --email $DJANGO_SUPERUSER_EMAIL
  fi
fi

# Start Gunicorn server for production
echo "Starting Gunicorn server..."
gunicorn LaundryTracker.wsgi:application --bind 0.0.0.0:8000 --workers 2
