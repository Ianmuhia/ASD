from django.test import TestCase
from django.test import SimpleTestCase


class SimpleTests(TestCase):
    def test_login_page_status_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_register_page_status_code(self):
        response = self.client.get('/regsiter/')
        self.assertEqual(response.status_code, 200)
