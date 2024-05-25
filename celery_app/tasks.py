from .celery import app
from minify.models import UrlMapping
from django.utils import timezone


@app.task
def update_is_active():
    number_of_updates = 0
    print("Task is running...")

    # gets all the objects
    query_set = UrlMapping.objects.filter(is_active=True)

    for item in query_set:
        if (timezone.now() - item.expires_at).days > 30:
            number_of_updates += 1
            item.is_active = False
            item.save()

    print(f"Total number of records updated: {number_of_updates}")
    print("Task is done...")


