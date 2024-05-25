from typing import Union
from django.utils import timezone
from django.db import models, transaction


class UrlMappingManager(models.Manager):
    def create_record(self, long_url: str, short_code: str) -> None:
        self.create(long_url=long_url, short_code=short_code)

    def update_record_and_get_long_url(self, short_code: str) -> Union[str, None]:
        record = self.filter(short_code=short_code, is_active=True)

        if not record:
            return None

        record = record[0]
        with transaction.atomic():
            record.total_visits += 1
            record.last_visit = timezone.now()
            record.expires_at = timezone.now() + timezone.timedelta(days=30)
            record.updated_at = timezone.now()
            record.save()

        return record.long_url
