#!/usr/bin/env bash
# Render build script
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# Seed sample content on first deploy (safe to re-run, uses update_or_create)
python manage.py seed_data

# Create/update the admin user so it always matches the DJANGO_SUPERUSER_*
# env vars. Running this on every deploy means the password can never drift
# out of sync with what's shown in the Render dashboard's Environment tab.
python manage.py shell -c "
from django.contrib.auth import get_user_model
import os
User = get_user_model()
username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'ChangeMe123!')
user, created = User.objects.get_or_create(username=username, defaults={'email': email})
user.email = email
user.is_staff = True
user.is_superuser = True
user.set_password(password)
user.save()
print('Superuser ready:', username, '(created)' if created else '(password reset)')
"