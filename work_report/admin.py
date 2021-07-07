from django.contrib import admin

from . import models

# Register your models here.

admin.site.register(models.Project)
admin.site.register(models.TypeOfWork)
admin.site.register(models.WorkReport)
