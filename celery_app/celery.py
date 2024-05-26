# tasks/celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'url_shortener.settings')

app = Celery('celery_app')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


# periodic tasks schedule
app.conf.beat_schedule = {
    'update-db-everyday-noon': {
        'task': 'celery_app.tasks.update_is_active',
        'schedule': crontab(hour='12', minute='00'),
    },
}

timezone = settings.TIME_ZONE
