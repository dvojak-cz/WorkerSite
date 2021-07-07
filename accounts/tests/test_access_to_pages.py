from django.test import TestCase, Client
from django.urls import reverse

from accounts.models import CustomUser


class TestNotLoggedUsers(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()

    def test_login_page(self):
        response = self.client.get(reverse('login-AC'))
        self.assertEqual(response.status_code, 200)

    def test_logout_page(self):
        response = self.client.get(reverse('logout-AC'))
        self.assertEqual(response.status_code, 302)


class TeslLoggedUser(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.user = CustomUser.objects.create_user(username="user",
                                                  password="password")

    def test_login_page(self):
        self.client.login(username="user", password="password")
        response = self.client.get(reverse('login-AC'))
        self.assertEqual(response.status_code, 302)

    def test_logout_page(self):
        self.client.login(username="user", password="password")
        response = self.client.get(reverse('logout-AC'))
        self.assertEqual(response.status_code, 302)
