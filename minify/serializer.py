from rest_framework import serializers
from django.core.validators import URLValidator
import logging

logger = logging.getLogger(__name__)


class CustomURLValidator(URLValidator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.schemes = ['http', 'https', 'ftp', 'ftps', '']

    def __call__(self, value):
        # If value has no scheme, prepend http:// to allow validation
        if '://' not in value:
            value = 'http://' + value
        super().__call__(value)


class MinifySerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    long_url = serializers.CharField(required=True, min_length=10, max_length=2000)

    @staticmethod
    def validate_long_url(long_url: str) -> str:
        validator = CustomURLValidator()

        try:
            validator(long_url)
        except Exception as e:
            logger.exception(f"exception: {e}")
            raise serializers.ValidationError(f'invalid URL: {e}')

        return long_url

