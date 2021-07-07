import django
from django.test import SimpleTestCase
from django.urls import reverse


class TestUrls(SimpleTestCase):

    def test_dashboard_WR_url(self):
        url = reverse('dashboard-WR')
        self.assertEqual(url, '/report/')

    def test_report_list_WR_url(self):
        url = reverse('report_list-WR')
        self.assertEqual(url, '/report/over_view/')

    def test_new_reports_WR_url(self):
        url = reverse('new_reports-WR')
        self.assertEqual(url, '/report/new/')

    def test_new_project_WR_url(self):
        url = reverse('new_project-WR')
        self.assertEqual(url, '/report/new_project/')

    def test_edit_report_WR_url(self):
        url = reverse('edit_report-WR', args=[1])
        self.assertEqual(url, '/report/edit/1/')
        try:
            url = reverse('edit_report-WR', args=['str'])
        except django.urls.exceptions.NoReverseMatch:
            return
        self.fail()

    def test_copy_report_WR_url(self):
        url = reverse('copy_report-WR', args=[1])
        self.assertEqual(url, '/report/copy/1/')
        try:
            url = reverse('copy_report-WR', args=['str'])
        except django.urls.exceptions.NoReverseMatch:
            return
        self.fail()

    def test_delete_report_WR_url(self):
        url = reverse('delete_report-WR', args=[1])
        self.assertEqual(url, '/report/delete/1/')
        try:
            url = reverse('delete_report-WR', args=['str'])
        except django.urls.exceptions.NoReverseMatch:
            return
        self.fail()

    def test_project_view_WR_url(self):
        url = reverse('project_view-WR')
        self.assertEqual(url, '/report/projects/')

    def test_export_csv_WR_url(self):
        url = reverse('export_csv-WR')
        self.assertEqual(url, '/report/export_csv/')

    def test_export_pdf_WR_url(self):
        url = reverse('export_pdf-WR')
        self.assertEqual(url, '/report/share_pdf/')
