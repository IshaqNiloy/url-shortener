from django.contrib import admin
from .models import UrlMapping


@admin.register(UrlMapping)
class UrlMappingAdmin(admin.ModelAdmin):
    list_display = ['id', 'long_url', 'short_code', 'total_visits', 'is_active', 'last_visit', 'expires_at',
                    'created_at', 'updated_at']
    list_filter = ['is_active']
    search_fields = ['id', 'long_url', 'short_code']
