from django.db import models


class UrlMappingManager(models.Manager):
    def create_record(self, long_url: str, short_code: str):
        self.create(long_url=long_url, short_code=short_code)
