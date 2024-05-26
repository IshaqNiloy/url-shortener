from django.utils import timezone
from django.db import models
from minify.manager import UrlMappingManager
from urllib.parse import urlparse
from django.core.exceptions import ValidationError


def get_expires_at():
    return timezone.now() + timezone.timedelta(days=30)


def validate_url(value):
    result = urlparse(value)
    if not all([result.scheme, result.netloc]):
        raise ValidationError(f'{value} is not a valid URL')


class UrlMapping(models.Model):
    id = models.AutoField(primary_key=True)
    long_url = models.URLField(max_length=10000, null=False,  validators=[validate_url])
    short_code = models.CharField(max_length=15, unique=True, null=False)
    total_visits = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    last_visit = models.DateTimeField(null=True, blank=True )
    expires_at = models.DateTimeField(default=get_expires_at, null=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    objects = UrlMappingManager()

    class Meta:
        verbose_name = 'Url Mapping'
        verbose_name_plural = 'Url Mappings'

        indexes = [
            models.Index(fields=['short_code']),
        ]

    def save(self, *args, **kwargs):
        parsed_url = urlparse(self.long_url)
        if not parsed_url.scheme:
            self.long_url = 'http://' + self.long_url
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Original Url: {self.long_url} -> Short Code: {self.short_code}"
