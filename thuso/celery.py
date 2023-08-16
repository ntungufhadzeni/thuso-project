import os

from celery import Celery
from celery.schedules import crontab

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

app.conf.update(timezone='Africa/Johannesburg')
# Load task modules from all registered Django apps.
app.autodiscover_tasks()

# CELERY BEAT SETTINGS

app.conf.beat_schedule = {
    'debug-task-every-day': {
        'task': 'cover_letter.tasks.debug_task',
        'schedule': crontab(hour=15, minute=56),
    }
}
