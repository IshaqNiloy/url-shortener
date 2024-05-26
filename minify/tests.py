from django.test import TestCase, Client
from url_shortener import settings
from .models import UrlMapping
from .views import MinifyView
from rest_framework import status
from utils.code_objects import REQUEST_FAILED, INVALID_REQUEST_DATA


class MinifyViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.minify_url = settings.BASE_URL + 'minify/'
        self.model = UrlMapping

    # tests short code length and uniqueness
    def test_get_short_code(self):
        num_of_iterations = 10000
        short_codes_length = set()
        short_codes = set()

        for i in range(num_of_iterations):
            minify_obj = MinifyView()
            short_code = minify_obj.get_short_code()
            short_codes_length.add(len(short_code))
            short_codes.add(short_code)

        self.assertEqual(len(short_codes), num_of_iterations)  # assert short code uniqueness
        self.assertEqual(len(short_codes_length), 1)  # assert all are of the same length
        self.assertEqual(list(short_codes_length)[0], int(settings.SHORT_CODE_LENGTH))  # assert the desired length of the short code

    # tests record creation
    def test_insert_record(self):
        minify_obj = MinifyView()
        long_url = 'https://www.upaybd.com'

        short_code = minify_obj.get_short_code()
        minify_obj.insert_record(long_url=long_url)

        self.assertTrue(self.model.objects.filter(short_code=short_code).exists())  # assert object exists

    # tests success response
    def test_success_response(self):
        request_payload = {
            "long_url": "https://www.google.com/"
        }
        response = self.client.post(self.minify_url, request_payload)
        url_mapping_obj = self.model.objects.filter(long_url=request_payload['long_url'])[0]
        short_url = response.json().get('data').get('short_url')

        self.assertEqual(response.status_code, status.HTTP_200_OK)  # assert status code
        self.assertIn('short_url', response.json().get('data'))  # assert short url key in data
        self.assertEqual(short_url, settings.BASE_URL+url_mapping_obj.short_code)  # assert short url

    # tests invalid request data response
    def test_invalid_request_data_response(self):
        request_payload = {
            "long_ur": "https://www.google.com/"
        }
        response = self.client.post(self.minify_url, request_payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)  # assert status code
        self.assertEqual(response.json(), INVALID_REQUEST_DATA)  # assert invalid request data response




