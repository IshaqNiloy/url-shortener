from django.test import TestCase, Client
from rest_framework import status

from minify.models import UrlMapping
from utils.code_objects import INVALID_REQUEST_DATA, DATA_NOT_FOUND
from .views import RedirectionView


class RedirectionViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.long_url = 'https://www.upaybd.com'
        self.short_code = 'HEcq1Z'
        self.url_mapping_obj = UrlMapping.objects.create(
            long_url=self.long_url,
            short_code=self.short_code,
        )

    # tests update functionality
    def test_db_operations(self):
        redirection_obj = RedirectionView()
        long_url = redirection_obj.db_operations(short_code=self.short_code)
        # gets updated object from the default database
        self.url_mapping_obj.refresh_from_db()

        self.assertEqual(self.long_url, long_url)  # assert long url
        self.assertEqual(self.url_mapping_obj.total_visits, 1)  # assert total visits

    # tests success response
    def test_success_response(self):
        response = self.client.get('/' + self.short_code)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)  # assert status code
        self.assertIn(self.long_url, response.headers['Location'])  # assert destination url

    # tests data not found response
    def test_data_not_found_response(self):
        response = self.client.get('/HEcq1C')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)  # assert status code
        self.assertEqual(response.json(), DATA_NOT_FOUND)  # assert data not found response

    # tests invalid request data response
    def test_invalid_request_data_response(self):
        response = self.client.get('/abbak')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)  # assert status code
        self.assertEqual(response.json(), INVALID_REQUEST_DATA)  # assert invalid request data response



