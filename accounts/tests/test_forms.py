from django.test import TestCase, Client
from django.urls import reverse

from accounts.models import CustomUser


class TesForms(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.user = CustomUser.objects.create_user(username="user",
                                                  password="password")

    def test_setLogOut(self):
        self.client.login(username="user", password="password")
        response = self.client.get(reverse('logout-AC'))
        self.assertEqual(response.status_code, 302)

    def test_setLogIn(self):
        response = self.client.post(reverse('login-AC'),
                                    {'username': 'user',
                                     'password': 'wrong'})
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('login-AC'),
                                    {'username': 'user',
                                     'password': 'password'})
        self.assertEqual(response.status_code, 302)
