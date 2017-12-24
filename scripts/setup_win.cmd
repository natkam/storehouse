@ECHO OFF
START /min cmd /k "manage.py runserver"
manage.py migrate
manage.py loaddata website/fixtures/full_random.json
ECHO Loaded data to the database.
ECHO from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'pass') | manage.py shell
