from django.test import SimpleTestCase
from django.urls import reverse


class TestUrls(SimpleTestCase):

    def test_login_url(self):
        url = reverse('login-AC')
        self.assertEqual(url, '/accounts/')

    def test_logout_url(self):
        url = reverse('logout-AC')
        self.assertEqual(url, '/accounts/logout/')

    def test_reset_password_url(self):
        url = reverse('reset_password')
        self.assertEqual(url, '/accounts/reset_password/')

    def test_password_reset_done_url(self):
        url = reverse('password_reset_done')
        self.assertEqual(url, '/accounts/reset_password_sent/')

    def test_password_reset_confirm_url(self):
        url = reverse('password_reset_confirm',
                      args=['MQ', 'akwfad-fea9a56ce344bbd426ba32e44fdb3984'])
        self.assertEqual(url,
                         '/accounts/reset/MQ/'
                         'akwfad-fea9a56ce344bbd426ba32e44fdb3984/')

    def test_password_reset_complete_url(self):
        url = reverse('password_reset_complete')
        self.assertEqual(url, '/accounts/reset_password_complete/')
