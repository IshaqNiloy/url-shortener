from rest_framework import serializers

from url_shortener import settings


class RedirectionViewSerializer(serializers.Serializer):
    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    short_code = serializers.CharField(required=True, min_length=int(settings.SHORT_CODE_LENGTH),
                                       max_length=int(settings.SHORT_CODE_LENGTH))
