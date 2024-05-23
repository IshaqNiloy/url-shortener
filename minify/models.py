from django.utils import timezone
from django.db import models
from manager import UrlMappingManager


class UrlMapping(models.Model):
    id = models.AutoField(primary_key=True)
    long_url = models.URLField(max_length=10000, null=False)
    short_code = models.CharField(max_length=15, unique=True, null=False)
    total_visits = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    last_visit = models.DateTimeField(null=True)
    expires_at = models.DateTimeField(default=lambda: timezone.now() + timezone.timedelta(days=30), null=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    objects = UrlMappingManager()

    class Meta:
        verbose_name = 'Url Mapping'
        verbose_name_plural = 'Url Mappings'

        indexes = [
            models.Index(fields=['short_code']),
        ]

    def __str__(self):
        return f"Original Url: {self.long_url} -> Short Code: {self.short_code}"
