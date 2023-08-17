import os

from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'thuso.settings')

app = Celery('thuso')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

app.control.enable_events(reply=True)

app.conf.enable_utc = False

# Set timezone for Celery
app.conf.timezone = 'Africa/Johannesburg'

# Specify the JSON serialization format
app.conf.accept_content = ['application/json']
app.conf.result_serializer = 'json'
app.conf.task_serializer = 'json'

# Configure the result backend to use Django database
app.conf.result_backend = 'django-db'

# Load task modules from all registered Django apps.
app.autodiscover_tasks()
