#!/bin/sh
set -e

python manage.py migrate --noinput
python manage.py collectstatic --noinput
python manage.py seed_data

python - <<'PY'
import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()
username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")
email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "")

if username and password:
    user, created = User.objects.get_or_create(
        username=username,
        defaults={"email": email, "is_staff": True, "is_superuser": True},
    )
    user.email = email or user.email
    user.is_staff = True
    user.is_superuser = True
    user.set_password(password)
    user.save()
    print(f"Superuser ready: {username} ({'created' if created else 'updated'})")
else:
    print("Skipping superuser: DJANGO_SUPERUSER_USERNAME/PASSWORD not set")
PY

PORT="${PORT:-8000}"
WORKERS="${GUNICORN_WORKERS:-3}"
exec gunicorn config.wsgi:application --bind "0.0.0.0:${PORT}" --workers "${WORKERS}" --timeout 60
