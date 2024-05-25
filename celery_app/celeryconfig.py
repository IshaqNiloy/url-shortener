from celery.schedules import crontab

broker_url = 'redis://localhost:6379/0'
result_backend = 'redis://localhost:6379/0'

beat_schedule = {
    'run-update-is-active-task-every-day-at-12:00PM': {
        'task': 'celery_app.tasks.update_is_active',
        'schedule': crontab(hour='12', minute='00'),
    },
}

timezone = 'UTC'
