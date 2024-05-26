import logging
from typing import Union

from django.http import HttpResponseRedirect
from rest_framework import status
from rest_framework.views import APIView

from minify.models import UrlMapping
from utils.code_objects import REQUEST_FAILED, INVALID_REQUEST_DATA, DATA_NOT_FOUND
from utils.response_helper import response
from .serializer import RedirectionViewSerializer

logger = logging.getLogger(__name__)


class RedirectionView(APIView):
    def __init__(self):
        super().__init__()
        self.model = UrlMapping
        self.serializer = RedirectionViewSerializer
        self.long_url = ''

    def db_operations(self, short_code: str) -> Union[str, None]:
        return self.model.objects.update_record_and_get_long_url(short_code=short_code)

    def get(self, request, **kwargs):
        try:
            self.serializer = self.serializer(data=kwargs)

            if self.serializer.is_valid():
                short_code = kwargs.get('short_code')
                # updates record and gets long url
                self.long_url = self.db_operations(short_code=short_code)
                logger.info(f'short code: {short_code} -> long url: {self.long_url}')

                if not self.long_url:
                    return response(code=DATA_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)

                return HttpResponseRedirect(self.long_url)
            else:
                return response(code=INVALID_REQUEST_DATA, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception(f'exception: {e}')
            return response(code=REQUEST_FAILED, status=status.HTTP_400_BAD_REQUEST)

