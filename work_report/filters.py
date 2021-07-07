import django_filters
from django.utils.translation import gettext_lazy as _
from django_filters import DateTimeFilter

from . import models


class WorkReportsFilter(django_filters.FilterSet):
    start = DateTimeFilter(field_name="arrival", lookup_expr='gte',
                           label=_("Od"))
    end = DateTimeFilter(field_name="arrival", lookup_expr='lte',
                         label=_("Do"))

    class Meta:
        model = models.WorkReport
        fields = ['worker', 'project', 'type_of_work', 'start', 'end']
