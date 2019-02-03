import os 
import sys
import django
from channels.asgi import get_channel_layer
from channels.routing import get_default_application
import config


sys.path.append(os.getcwd())

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
# django.setup()
channel_layer = get_channel_layer()
