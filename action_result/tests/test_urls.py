from django.test import SimpleTestCase
from django.urls import reverse


class TestUrls(SimpleTestCase):
    def test_unauthorised(self):
        url = reverse('unauthorised-AR')
        self.assertEqual(url, '/action/unauthorised/')
