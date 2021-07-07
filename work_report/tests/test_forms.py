import datetime

from django.contrib.auth.models import Group
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone

from accounts.models import CustomUser
from work_report.models import Project, TypeOfWork, WorkReport


class BaseClase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client_worker = Client()
        cls.client_admin = Client()
        group_worker = Group.objects.create(name="worker")
        group_admin = Group.objects.create(name="admin")

        cls.user_worker = CustomUser.objects.create_user(username="worker",
                                                         password="zDepa")
        cls.user_admin = CustomUser.objects.create_user(username="admin",
                                                        password="zDepa")
        cls.user_admin.groups.add(group_admin)
        cls.user_worker.groups.add(group_worker)

        cls.project = Project.objects.create(name="projekt1")
        cls.type = TypeOfWork.objects.create(label="type")

        cls.report_worker = WorkReport.objects. \
            create(worker=cls.user_worker,
                   description="des",
                   arrival=timezone.now(),
                   departure=timezone.now(),
                   productive_time=datetime.timedelta(),
                   type_of_work=cls.type,
                   project=cls.project,
                   )
        cls.report_admin = WorkReport.objects. \
            create(worker=cls.user_admin,
                   description="des",
                   arrival=timezone.now(),
                   departure=timezone.now(),
                   productive_time=datetime.timedelta(),
                   type_of_work=cls.type,
                   project=cls.project,
                   )


class TestDelete(BaseClase):
    def test_delete_own_admin(self):
        self.client_admin.login(username=self.user_admin.username,
                                password="zDepa")
        response = self.client_admin.post(
                reverse('delete_report-WR', args=[self.report_admin.pk]))
        self.assertEqual(
                WorkReport.objects.filter(pk=self.report_admin.pk).count(), 0)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('report_list-WR'))

    def test_delete_own_worker(self):
        self.client_worker.login(username=self.user_worker.username,
                                 password="zDepa")
        response = self.client_worker.post(
                reverse('delete_report-WR', args=[self.report_worker.pk]))
        self.assertEqual(
                WorkReport.objects.filter(pk=self.report_worker.pk).count(), 0)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('report_list-WR'))

    def test_delete_not_own_admin(self):
        self.client_admin.login(username=self.user_admin.username,
                                password="zDepa")
        response = self.client_admin.post(
                reverse('delete_report-WR', args=[self.report_worker.pk]))
        self.assertEqual(
                WorkReport.objects.filter(pk=self.report_worker.pk).count(), 0)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('report_list-WR'))

    def test_delete_not_own_worker(self):
        self.client_worker.login(username=self.user_worker.username,
                                 password="zDepa")
        response = self.client_worker.post(
                reverse('delete_report-WR', args=[self.report_admin.pk]))
        self.assertEqual(
                WorkReport.objects.filter(pk=self.report_worker.pk).count(), 1)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('unauthorised-AR'))


class TestEdit(BaseClase):
    def test_edit_own_admin(self):
        self.client_admin.login(username=self.user_admin.username,
                                password="zDepa")
        response = self.client_admin.post(
                reverse('edit_report-WR', args=[self.report_admin.pk]), {
                    'worker': self.user_admin.pk,
                    'description': 'popis_ted',
                    'arrival': timezone.now(),
                    'departure': timezone.now(),
                    'productive_time_0': 1,
                    'productive_time_1': 2,
                    'type_of_work': self.type.pk,
                    'project': self.project.pk, })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('report_list-WR'))
        self.assertEqual(1, WorkReport.objects.filter(
                description='popis_ted').count())

    def test_edit_own_worker(self):
        self.client_worker.login(username=self.user_worker.username,
                                 password="zDepa")
        response = self.client_worker.post(
                reverse('edit_report-WR', args=[self.report_worker.pk]), {
                    'worker': self.user_worker.pk,
                    'description': 'popis_ted',
                    'arrival': timezone.now(),
                    'departure': timezone.now(),
                    'productive_time_0': 1,
                    'productive_time_1': 2,
                    'type_of_work': self.type.pk,
                    'project': self.project.pk, })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('report_list-WR'))
        self.assertEqual(1, WorkReport.objects.filter(
                description='popis_ted').count())

    def test_edit_not_own_admin(self):
        self.client_admin.login(username=self.user_admin.username,
                                password="zDepa")
        response = self.client_admin.post(
                reverse('edit_report-WR', args=[self.report_worker.pk]), {
                    'worker': self.user_worker.pk,
                    'description': 'popis_ted',
                    'arrival': timezone.now(),
                    'departure': timezone.now(),
                    'productive_time_0': 1,
                    'productive_time_1': 2,
                    'type_of_work': self.type.pk,
                    'project': self.project.pk, })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('report_list-WR'))
        self.assertEqual(1, WorkReport.objects.filter(
                description='popis_ted').count())

    def test_edit_not_own_worker(self):
        self.client_worker.login(username=self.user_worker.username,
                                 password="zDepa")
        response = self.client_worker.post(
                reverse('edit_report-WR', args=[self.report_admin.pk]), {
                    'worker': self.user_admin.pk,
                    'description': 'popis_ted',
                    'arrival': timezone.now(),
                    'departure': timezone.now(),
                    'productive_time_0': 1,
                    'productive_time_1': 2,
                    'type_of_work': self.type.pk,
                    'project': self.project.pk, })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('unauthorised-AR'))
        self.assertEqual(0, WorkReport.objects.filter(
                description='popis_ted').count())


class TestNewReport(BaseClase):
    def test_own_report_admin(self):
        self.client_admin.login(username=self.user_admin.username,
                                password="zDepa")
        response = self.client_admin.post(reverse('new_reports-WR'), {
            'worker': self.user_admin.pk,
            'description': 'popis_ted',
            'arrival': timezone.now(),
            'departure': timezone.now(),
            'productive_time_0': 1,
            'productive_time_1': 2,
            'type_of_work': self.type.pk,
            'project': self.project.pk, })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('report_list-WR'))
        self.assertEqual(1, WorkReport.objects.filter(
                description='popis_ted').count())

    def test_own_report_worker(self):
        self.client_worker.login(username=self.user_worker.username,
                                 password="zDepa")
        response = self.client_worker.post(reverse('new_reports-WR'), {
            'worker': self.user_worker.pk,
            'description': 'popis_ted',
            'arrival': timezone.now(),
            'departure': timezone.now(),
            'productive_time_0': 1,
            'productive_time_1': 2,
            'type_of_work': self.type.pk,
            'project': self.project.pk, })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('report_list-WR'))
        self.assertEqual(1, WorkReport.objects.filter(
                description='popis_ted').count())

    def test_not_own_report_admin(self):
        self.client_admin.login(username=self.user_admin.username,
                                password="zDepa")
        response = self.client_admin.post(reverse('new_reports-WR'), {
            'worker': self.user_worker.pk,
            'description': 'popis_ted',
            'arrival': timezone.now(),
            'departure': timezone.now(),
            'productive_time_0': 1,
            'productive_time_1': 2,
            'type_of_work': self.type.pk,
            'project': self.project.pk, })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('report_list-WR'))
        self.assertEqual(1, WorkReport.objects.filter(
                description='popis_ted').count())

    def test_not_own_report_worker(self):
        self.client_worker.login(username=self.user_worker.username,
                                 password="zDepa")
        response = self.client_worker.post(reverse('new_reports-WR'), {
            'worker': self.user_admin.pk,
            'description': 'popis_ted',
            'arrival': timezone.now(),
            'departure': timezone.now(),
            'productive_time_0': 1,
            'productive_time_1': 2,
            'type_of_work': self.type.pk,
            'project': self.project.pk, })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('unauthorised-AR'))
        self.assertEqual(0, WorkReport.objects.filter(
                description='popis_ted').count())


class TestCopy(BaseClase):
    def test_copy_own_admin(self):
        self.client_admin.login(username=self.user_admin.username,
                                password="zDepa")
        response = self.client_admin.post(
                reverse('copy_report-WR', args=[self.report_admin.pk]), {
                    'worker': self.user_admin.pk,
                    'description': 'popis_ted',
                    'arrival': timezone.now(),
                    'departure': timezone.now(),
                    'productive_time_0': 1,
                    'productive_time_1': 2,
                    'type_of_work': self.type.pk,
                    'project': self.project.pk, })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('report_list-WR'))
        self.assertEqual(1, WorkReport.objects.filter(
                description='popis_ted').count())

    def test_copy_own_worker(self):
        self.client_worker.login(username=self.user_worker.username,
                                 password="zDepa")
        response = self.client_worker.post(
                reverse('copy_report-WR', args=[self.report_worker.pk]), {
                    'worker': self.user_worker.pk,
                    'description': 'popis_ted',
                    'arrival': timezone.now(),
                    'departure': timezone.now(),
                    'productive_time_0': 1,
                    'productive_time_1': 2,
                    'type_of_work': self.type.pk,
                    'project': self.project.pk, })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('report_list-WR'))
        self.assertEqual(1, WorkReport.objects.filter(
                description='popis_ted').count())

    def test_copy_not_own_admin(self):
        self.client_admin.login(username=self.user_admin.username,
                                password="zDepa")
        response = self.client_admin.post(
                reverse('copy_report-WR', args=[self.report_worker.pk]), {
                    'worker': self.user_worker.pk,
                    'description': 'popis_ted',
                    'arrival': timezone.now(),
                    'departure': timezone.now(),
                    'productive_time_0': 1,
                    'productive_time_1': 2,
                    'type_of_work': self.type.pk,
                    'project': self.project.pk, })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('report_list-WR'))
        self.assertEqual(1, WorkReport.objects.filter(
                description='popis_ted').count())

    def test_copy_not_own_worker(self):
        self.client_worker.login(username=self.user_worker.username,
                                 password="zDepa")
        response = self.client_worker.post(
                reverse('copy_report-WR', args=[self.report_admin.pk]), {
                    'worker': self.user_admin.pk,
                    'description': 'popis_ted',
                    'arrival': timezone.now(),
                    'departure': timezone.now(),
                    'productive_time_0': 1,
                    'productive_time_1': 2,
                    'type_of_work': self.type.pk,
                    'project': self.project.pk, })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('report_list-WR'))
        self.assertEqual(1, WorkReport.objects.filter(
                description='popis_ted').count())
