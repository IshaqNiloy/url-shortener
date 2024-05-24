from rest_framework import serializers
from django.core.validators import URLValidator
from rest_framework.exceptions import ValidationError


class MinifySerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    long_url = serializers.CharField(required=True, min_length=10, max_length=2000)

    @staticmethod
    def validate_long_url(url):
        validator = URLValidator()

        try:
            validator(url)
        except ValidationError:
            raise ValidationError('invalid URL')

        return url
