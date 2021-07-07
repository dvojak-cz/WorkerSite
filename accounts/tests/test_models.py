import sqlite3

from django.db import utils
from django.test import TestCase

# Create your tests here.
from accounts.models import CustomUser


class TestCustomUser(TestCase):

    @classmethod
    def setUpTestData(cls):
        CustomUser.objects.create(password='secretPassword',
                                  is_superuser=False,
                                  username='John',
                                  first_name='Fr',
                                  last_name='Om',
                                  email='FrOm@gmail.com',
                                  is_staff=False,
                                  is_active=True)

    def test_unique_id(self):
        try:
            user_id = CustomUser.objects.first().id
            CustomUser.objects.create(id=user_id)
        except (utils.IntegrityError, sqlite3.IntegrityError):
            return
        self.fail()

    def test_unique_username(self):
        try:
            username = CustomUser.objects.first().username
            CustomUser.objects.create(username=username)
        except (utils.IntegrityError, sqlite3.IntegrityError):
            return
        self.fail()
