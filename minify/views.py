import logging
import string
import time
import secrets
from rest_framework.views import APIView
from minify.models import UrlMapping
from rest_framework import status
from rest_framework.response import Response
from abc import ABC, abstractmethod

from url_shortener import settings
from utils.response_helper import response
from utils.code_objects import REQUEST_SUCCESS, REQUEST_FAILED, INVALID_REQUEST_DATA
from minify.serializer import MinifySerializer

logger = logging.getLogger(__name__)

# class (ABC):
#     @abstractmethod
#     def

class MinifyView(APIView):
    ALPHANUMERIC_POOL = string.ascii_letters + string.digits

    def __init__(self):
        super().__init__()
        self.model = UrlMapping
        self.serializer = MinifySerializer
        self.short_code = ''

    def get_short_code(self) -> str:
        # generates a cryptographically secure random number
        random_bytes = secrets.token_bytes(nbytes=int(settings.NUMBER_OF_BYTES))
        # Convert bytes to integer
        num = int.from_bytes(random_bytes, byteorder='big', signed=False)
        pool_length = len(MinifyView.ALPHANUMERIC_POOL)

        while num:
            num, remainder = divmod(num, pool_length)
            self.short_code += MinifyView.ALPHANUMERIC_POOL[remainder]

        return self.short_code[:int(settings.SHORT_URL_LENGTH)]

    def insert_record(self, long_url: str):
        self.model.objects.create_record(long_url=long_url, short_code=self.short_code)

    def post(self, request):
        try:
            self.serializer = self.serializer(data=request.data)

            if self.serializer.is_valid():
                # gets short code
                self.short_code = self.get_short_code()
                logger.info(f'short code: {self.short_code}')
                # inserts record
                self.insert_record(long_url=self.serializer.validated_data['long_url'])
                logger.info('db insertion success')
                data = {'short_url': settings.BASE_URL + self.short_code}

                return response(code=REQUEST_SUCCESS, data=data, status=status.HTTP_200_OK)
            else:
                return response(code=INVALID_REQUEST_DATA, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception(f'exception: {e}')
            return response(code=REQUEST_FAILED, status=status.HTTP_400_BAD_REQUEST)

