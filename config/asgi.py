import os 
import sys
import django
from channels.routing import get_default_application


sys.path.append(os.getcwd())

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
application = get_default_application()
