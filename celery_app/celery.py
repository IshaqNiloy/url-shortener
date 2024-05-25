# tasks/celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'url_shortener.settings')

app = Celery('celery_app')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


# Define the periodic tasks schedule
app.conf.beat_schedule = {
    'update-db-everyday-noon': {
        'task': 'celery_app.tasks.update_is_active',
        'schedule': crontab(hour=19, minute=30),
        'args': (),
    },
}

