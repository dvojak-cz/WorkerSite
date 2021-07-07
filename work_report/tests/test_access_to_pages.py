import datetime

from django.contrib.auth.models import Group
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone

from accounts.models import CustomUser
from work_report.models import Project, TypeOfWork, WorkReport


class TestNotLoggedUsers(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()

    def test_dash_board_redirect_unloged_user(self):
        responce = self.client.get(reverse('dashboard-WR'))
        self.assertEqual(responce.status_code, 302)

    def test_report_list_redirect_unloged_user(self):
        responce = self.client.get(reverse('report_list-WR'))
        self.assertEqual(responce.status_code, 302)

    def test_new_reports_redirect_unloged_user(self):
        responce = self.client.get(reverse('new_reports-WR'))
        self.assertEqual(responce.status_code, 302)

    def test_new_project_redirect_unloged_user(self):
        responce = self.client.get(reverse('new_project-WR'))
        self.assertEqual(responce.status_code, 302)

    def test_edit_report_redirect_unloged_user(self):
        responce = self.client.get(reverse('edit_report-WR', args=[1]))
        self.assertEqual(responce.status_code, 302)

    def test_copy_report_redirect_unloged_user(self):
        responce = self.client.get(reverse('copy_report-WR', args=[1]))
        self.assertEqual(responce.status_code, 302)

    def test_delete_report_redirect_unloged_user(self):
        responce = self.client.get(reverse('delete_report-WR', args=[1]))
        self.assertEqual(responce.status_code, 302)

    def test_project_view_redirect_unloged_user(self):
        responce = self.client.get(reverse('project_view-WR'))
        self.assertEqual(responce.status_code, 302)

    def test_export_csv_redirect_unloged_user(self):
        responce = self.client.get(reverse('export_csv-WR'))
        self.assertEqual(responce.status_code, 302)

    def test_export_pdf_redirect_unloged_user(self):
        responce = self.client.get(reverse('export_pdf-WR'))
        self.assertEqual(responce.status_code, 302)


class TestNonGroup(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.user = CustomUser.objects.create_user(username="user",
                                                  password="password")

    def test_dashboard(self):
        self.client.login(username="user", password="password")
        response = self.client.get(reverse('dashboard-WR'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('unauthorised-AR'))

    def test_report_list(self):
        self.client.login(username="user", password="password")
        response = self.client.get(reverse('report_list-WR'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('unauthorised-AR'))

    def test_new_reports(self):
        self.client.login(username="user", password="password")
        response = self.client.get(reverse('new_reports-WR'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('unauthorised-AR'))

    def test_new_project(self):
        self.client.login(username="user", password="password")
        response = self.client.get(reverse('new_project-WR'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('unauthorised-AR'))

    def test_edit_report(self):
        self.client.login(username="user", password="password")
        response = self.client.get(reverse('edit_report-WR', args=[1]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('unauthorised-AR'))

    def test_copy_report(self):
        self.client.login(username="user", password="password")
        response = self.client.get(reverse('copy_report-WR', args=[1]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('unauthorised-AR'))

    def test_delete_report(self):
        self.client.login(username="user", password="password")
        response = self.client.get(reverse('delete_report-WR', args=[1]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('unauthorised-AR'))

    def test_project_view(self):
        self.client.login(username="user", password="password")
        response = self.client.get(reverse('project_view-WR'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('unauthorised-AR'))

    def test_export_csv(self):
        self.client.login(username="user", password="password")
        response = self.client.get(reverse('export_csv-WR'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('unauthorised-AR'))

    def test_export_pdf(self):
        self.client.login(username="user", password="password")
        response = self.client.get(reverse('export_pdf-WR'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('unauthorised-AR'))


class TestAminGroup(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        group = Group.objects.create(name="admin")
        user = CustomUser.objects.create_user(username="user",
                                              password="password")
        user.groups.add(group)

        project = Project.objects.create(name="projekt1")
        type = TypeOfWork.objects.create(label="type")
        cls.report = WorkReport.objects. \
            create(worker=user,
                   description="des",
                   arrival=timezone.now(),
                   departure=timezone.now(),
                   productive_time=datetime.timedelta(),
                   type_of_work=type,
                   project=project,
                   )

    def test_dashboard(self):
        self.client.login(username="user", password="password")
        response = self.client.get(reverse('dashboard-WR'))
        self.assertEqual(response.status_code, 200)

    def test_report_list(self):
        self.client.login(username="user", password="password")
        response = self.client.get(reverse('report_list-WR'))
        self.assertEqual(response.status_code, 200)

    def test_new_reports(self):
        self.client.login(username="user", password="password")
        response = self.client.get(reverse('new_reports-WR'))
        self.assertEqual(response.status_code, 200)

    def test_new_project(self):
        self.client.login(username="user", password="password")
        response = self.client.get(reverse('new_project-WR'))
        self.assertEqual(response.status_code, 200)

    def test_edit_report(self):
        self.client.login(username="user", password="password")
        response = self.client.get(
                reverse('edit_report-WR', args=[self.report.pk]))
        self.assertEqual(response.status_code, 200)

    def test_copy_report(self):
        self.client.login(username="user", password="password")
        response = self.client.get(
                reverse('copy_report-WR', args=[self.report.pk]))
        self.assertEqual(response.status_code, 200)

    def test_delete_report(self):
        self.client.login(username="user", password="password")
        response = self.client.get(
                reverse('delete_report-WR', args=[self.report.pk]))
        self.assertEqual(response.status_code, 200)

    def test_project_view(self):
        self.client.login(username="user", password="password")
        response = self.client.get(reverse('project_view-WR'))
        self.assertEqual(response.status_code, 200)

    def test_export_csv(self):
        self.client.login(username="user", password="password")
        response = self.client.get(reverse('export_csv-WR'))
        self.assertEqual(response.status_code, 200)

    def test_export_pdf(self):
        self.client.login(username="user", password="password")
        response = self.client.get(reverse('export_pdf-WR'))
        self.assertEqual(response.status_code, 200)


class TestWorkerGroup(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        group = Group.objects.create(name="worker")
        user = CustomUser.objects.create_user(username="user",
                                              password="password")
        user.groups.add(group)
        project = Project.objects.create(name="projekt1")
        type = TypeOfWork.objects.create(label="type")
        cls.report = WorkReport.objects. \
            create(worker=user,
                   description="des",
                   arrival=timezone.now(),
                   departure=timezone.now(),
                   productive_time=datetime.timedelta(),
                   type_of_work=type,
                   project=project,
                   )

    def test_dashboard(self):
        self.client.login(username="user", password="password")
        response = self.client.get(reverse('dashboard-WR'))
        self.assertEqual(response.status_code, 200)

    def test_report_list(self):
        self.client.login(username="user", password="password")
        response = self.client.get(reverse('report_list-WR'))
        self.assertEqual(response.status_code, 200)

    def test_new_reports(self):
        self.client.login(username="user", password="password")
        response = self.client.get(reverse('new_reports-WR'))
        self.assertEqual(response.status_code, 200)

    def test_new_project(self):
        self.client.login(username="user", password="password")
        response = self.client.get(reverse('new_project-WR'))
        self.assertEqual(response.status_code, 200)

    def test_edit_report(self):
        self.client.login(username="user", password="password")
        response = self.client.get(
                reverse('edit_report-WR', args=[self.report.pk]))
        self.assertEqual(response.status_code, 200)

    def test_copy_report(self):
        self.client.login(username="user", password="password")
        response = self.client.get(
                reverse('copy_report-WR', args=[self.report.pk]))
        self.assertEqual(response.status_code, 200)

    def test_delete_report(self):
        self.client.login(username="user", password="password")
        response = self.client.get(
                reverse('delete_report-WR', args=[self.report.pk]))
        self.assertEqual(response.status_code, 200)

    def test_project_view(self):
        self.client.login(username="user", password="password")
        response = self.client.get(reverse('project_view-WR'))
        self.assertEqual(response.status_code, 200)

    def test_export_csv(self):
        self.client.login(username="user", password="password")
        response = self.client.get(reverse('export_csv-WR'))
        self.assertEqual(response.status_code, 200)

    def test_export_pdf(self):
        self.client.login(username="user", password="password")
        response = self.client.get(reverse('export_pdf-WR'))
        self.assertEqual(response.status_code, 200)


class TestSuperuserAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        group = Group.objects.create(name="admin")
        user = CustomUser.objects.create_user(username="user",
                                              password="password")
        user_diffrent = CustomUser.objects.create_user(username="Pepa",
                                                       password="zDepa")
        user.groups.add(group)

        project = Project.objects.create(name="projekt1")
        type = TypeOfWork.objects.create(label="type")
        cls.report = WorkReport.objects. \
            create(worker=user_diffrent,
                   description="des",
                   arrival=timezone.now(),
                   departure=timezone.now(),
                   productive_time=datetime.timedelta(),
                   type_of_work=type,
                   project=project,
                   )

    def test_edit_report(self):
        self.client.login(username="user", password="password")
        response = self.client.get(
                reverse('edit_report-WR', args=[self.report.pk]))
        self.assertEqual(response.status_code, 200)

    def test_copy_report(self):
        self.client.login(username="user", password="password")
        response = self.client.get(
                reverse('copy_report-WR', args=[self.report.pk]))
        self.assertEqual(response.status_code, 200)

    def test_delete_report(self):
        self.client.login(username="user", password="password")
        response = self.client.get(
                reverse('delete_report-WR', args=[self.report.pk]))
        self.assertEqual(response.status_code, 200)


class TestNotSuperuserAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        group = Group.objects.create(name="worker")
        user = CustomUser.objects.create_user(username="user",
                                              password="password")
        user_diffrent = CustomUser.objects.create_user(username="Pepa",
                                                       password="zDepa")
        user.groups.add(group)

        project = Project.objects.create(name="projekt1")
        type = TypeOfWork.objects.create(label="type")
        cls.report = WorkReport.objects.create(worker=user_diffrent,
                                               description="des",
                                               arrival=timezone.now(),
                                               departure=timezone.now(),
                                               productive_time=datetime.timedelta(),
                                               type_of_work=type,
                                               project=project,
                                               )

    def test_edit_report(self):
        self.client.login(username="user", password="password")
        response = self.client.get(
                reverse('edit_report-WR', args=[self.report.pk]))
        self.assertEqual(response.status_code, 302)

    def test_copy_report(self):
        self.client.login(username="user", password="password")
        response = self.client.get(
                reverse('copy_report-WR', args=[self.report.pk]))
        self.assertEqual(response.status_code, 200)

    def test_delete_report(self):
        self.client.login(username="user", password="password")
        response = self.client.get(
                reverse('delete_report-WR', args=[self.report.pk]))
        self.assertEqual(response.status_code, 302)
