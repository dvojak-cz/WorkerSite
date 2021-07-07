from datetime import timedelta

from django.db import models

from accounts.models import CustomUser


class Project(models.Model):
    id = models.AutoField(primary_key=True, null=False, unique=True)
    name = models.CharField(max_length=255, null=False, unique=True)

    def __str__(self):
        if len(self.name) > 20:
            return self.name[:20 - 3] + '...'
        else:
            return self.name

    def __repr__(self):
        return f"Project(name={self.name})"


class TypeOfWork(models.Model):
    id = models.AutoField(primary_key=True, null=False, unique=True)
    label = models.CharField(max_length=255, null=False, unique=True)

    def __str__(self):
        if len(self.label) > 20:
            return self.label[:20 - 3] + '...'
        else:
            return self.label

    def __repr__(self):
        return f"TypeOfWork(label={self.label})"


class WorkReport(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    worker = models.ForeignKey(CustomUser, null=True,
                               on_delete=models.SET_NULL)
    description = models.TextField(null=False)
    arrival = models.DateTimeField(null=False)
    departure = models.DateTimeField(null=False)
    productive_time = models.DurationField(default=timedelta())
    type_of_work = models.ForeignKey(TypeOfWork, null=True,
                                     on_delete=models.SET_NULL)
    project = models.ForeignKey(Project, null=True, on_delete=models.SET_NULL)
    creat_time = models.DateTimeField(auto_now_add=True, null=False)
    edit_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        if len(self.description) > 30:
            return self.description[:30 - 3] + '...'
        else:
            return self.description

    def __repr__(self):
        return f"WorkCategory(worker={self.worker}, " \
               f"description={self.description}, " \
               f"arrival={self.arrival}, " \
               f"departure={self.departure}, " \
               f"productive_time={self.productive_time}, " \
               f"type_of_work={self.type_of_work}, " \
               f"project={self.project}, " \
               f"creat_time = {self.creat_time}, " \
               f"edit_time = {self.edit_time}) "
