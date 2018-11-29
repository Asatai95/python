import os
import sys

from django.core.wsgi import get_wsgi_application

sys.path.append('/var/www/django/config')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()
