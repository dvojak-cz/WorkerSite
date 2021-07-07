import datetime

from django.test import TestCase
# Create your tests here.
from django.utils import timezone

from accounts.models import CustomUser
from work_report.models import Project, TypeOfWork, WorkReport


class ProjectTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Project.objects.create(name="testovaci name")

    def test_unique_name(self):
        try:
            name = Project.objects.first().name
            Project.objects.create(name=name)
        except:
            return
        self.fail()

    def test_not_null_name(self):
        try:
            Project.objects.create(name=None)
        except:
            return
        self.fail()


class TypeOfWorkTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        TypeOfWork.objects.create(label="testovaci label")

    def test_unique_label(self):
        try:
            label = TypeOfWork.objects.first().label
            TypeOfWork.objects.create(label=label)
        except:
            return
        self.fail()

    def test_not_null_label(self):
        try:
            TypeOfWork.objects.create(label=None)
        except:
            return
        self.fail()


class WorkReportTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.project = Project.objects.create(name="p1")
        cls.type = TypeOfWork.objects.create(label="t1")
        cls.worker = CustomUser.objects.create(username="u1")
        cls.report = WorkReport.objects. \
            create(worker=cls.worker,
                   description="des",
                   arrival=timezone.now(),
                   departure=timezone.now(),
                   productive_time=datetime.timedelta(),
                   type_of_work=cls.type,
                   project=cls.project,
                   )

    def test_nullable_worker(self):
        self.report.worker = None
        self.report.save()
        self.assertEqual(self.report.worker, None)

    def test_nullable_type_of_work(self):
        self.report.type_of_work = None
        self.report.save()
        self.assertEqual(self.report.type_of_work, None)

    def test_nullable_project(self):
        self.report.project = None
        self.report.save()
        self.assertEqual(self.report.project, None)

    def test_not_nullable_description(self):
        try:
            self.report.description = None
            self.report.save()
        except:
            return
        self.fail()

    def test_not_nullable_arrival(self):
        try:
            self.report.arrival = None
            self.report.save()
        except:
            return
        self.fail()

    def test_not_nullable_departure(self):
        try:
            self.report.departure = None
            self.report.save()
        except:
            return
        self.fail()

    def test_not_nullable_productive_time(self):
        try:
            self.report.productive_time = None
            self.report.save()
        except:
            return
        self.fail()

    def test_not_nullable_creat_time(self):
        try:
            self.report.creat_time = None
            self.report.save()
        except:
            return
        self.fail()

    def test_not_nullable_edit_time(self):
        self.report.edit_time = None
        self.report.save()
        self.assertNotEqual(self.report.edit_time, None)

    def test_on_delete_worker(self):
        self.assertNotEqual(self.report.worker, None)
        self.worker.delete()
        self.assertEqual(WorkReport.objects.filter(pk=self.report.pk)
                         .values('worker')[0]['worker'], None)

    def test_on_delete_type_of_work(self):
        self.assertNotEqual(self.report.type_of_work, None)
        self.type.delete()
        self.assertEqual(WorkReport.objects.filter(pk=self.report.pk)
                         .values('type_of_work')[0]['type_of_work'], None)

    def test_on_delete_worker(self):
        self.assertNotEqual(self.report.project, None)
        self.project.delete()
        self.assertEqual(WorkReport.objects.filter(pk=self.report.pk)
                         .values('project')[0]['project'], None)
