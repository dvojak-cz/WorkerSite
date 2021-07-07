from django import forms
from django.utils.translation import gettext_lazy as _
from durationwidget.widgets import TimeDurationWidget

from . import models


class NewWorkReportForm(forms.ModelForm):
    class Meta:
        model = models.WorkReport
        fields = ['worker',
                  'description',
                  'arrival',
                  'departure',
                  'productive_time',
                  'type_of_work',
                  'project']
        widgets = {
            'worker': forms.Select(),
            'name': forms.Textarea(),

            'arrival': forms.DateTimeInput(),
            'departure': forms.DateTimeInput(),

            'project': forms.Select(),
            'type_of_work': forms.Select(),

            'productive_time': TimeDurationWidget(show_days=False,
                                                  show_seconds=False),
            }
        labels = {
            'worker': _('Pracovník'),
            'name': _('Činnost'),
            'arrival': _('Příchod'),
            'departure': _('Odchod'),
            'productive_time': _('Produktivní čas'),
            'type_of_work': _('Druh práce'),
            'project': _('Projekt'),
            }
        help_texts = {
            'worker': _('Jméno pracovníka'),
            'name': _('Popis odvedené práce'),
            'arrival': _('Čas příchodu do práce'),
            'departure': _('Čas odchodu z práce'),
            'productive_time': _('Čistý čas práce'),
            'type_of_work': _('Druh práce'),
            'project': _('Projekt na kterém jste pracoval'),
            }


class NewProjectForm(forms.ModelForm):
    class Meta:
        model = models.Project
        fields = ['name']
        labels = {
            'name': _('Název'),
            }
