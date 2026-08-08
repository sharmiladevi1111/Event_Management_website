#!/usr/bin/env bash
# Render build script
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# Seed sample content on first deploy (safe to re-run, uses update_or_create)
python manage.py seed_data

# Create a default admin user if one doesn't already exist.
# Override credentials with DJANGO_SUPERUSER_* env vars on Render.
python manage.py shell -c "
from django.contrib.auth import get_user_model
import os
User = get_user_model()
username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'ChangeMe123!')
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print('Superuser created:', username)
else:
    print('Superuser already exists:', username)
"
