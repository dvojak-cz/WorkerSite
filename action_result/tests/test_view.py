from django.test import TestCase, Client
from django.urls import reverse


class TestView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()

    def test_unauthorised(self):
        response = self.client.get(reverse('unauthorised-AR'))
        self.assertEqual(response.status_code, 200)
