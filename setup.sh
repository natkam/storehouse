#!/usr/bin/env bash

python manage.py runserver
python manage.py migrate
python manage.py loaddata website/fixtures/full_random.json
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'pass')" | ./manage.py shell
