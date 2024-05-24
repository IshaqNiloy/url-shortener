import logging
from rest_framework.views import APIView
from minify.models import UrlMapping
from rest_framework import status
from rest_framework.response import Response
from abc import ABC, abstractmethod

from minify.serializer import MinifySerializer

logger = logging.getLogger(__name__)


# class (ABC):
#     @abstractmethod
#     def

class MinifyView(APIView):
    def __init__(self):
        super().__init__()
        self.model = UrlMapping
        self.serializer = MinifySerializer

    def get_short_code(self):
        pass

    def post(self, request):
        try:
            self.serializer = self.serializer(data=request.data)

            if self.serializer.is_valid():
                self.get_short_code()
            return Response(data={}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception(f'exception: {e}')

