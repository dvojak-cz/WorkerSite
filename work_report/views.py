import csv
import logging
import tempfile

import django as django
from dateutil.relativedelta import relativedelta
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from weasyprint import HTML

from . import filters
from . import forms
from . import models
from .decorators import (allowed_users, allow_submit_own_data_post,
                         allow_edit_own_data_page, )
from .utils import get_plot_cake, get_plot_normal


@login_required(login_url='login-AC')
@allowed_users(allowed_groups={'admin', 'worker'})
def export_to_csv(request):
    responce = HttpResponse(content_type='text/csv')

    responce['Content-Disposition'] = 'attachment; filename=Work_Report-' + \
                                      str(timezone.now()) + '.csv'

    writer = csv.writer(responce)
    writer.writerow(['worker', 'description', 'arrival', 'departure',
                     'productive_time', 'type_of_work', 'project',
                     'creat_time', 'edit_time', ])

    data = models.WorkReport.objects.all()
    if request.method == "GET":
        work_report_filter = filters.WorkReportsFilter(request.GET,
                                                       queryset=data)
        data = work_report_filter.qs

    for rep in data:
        writer.writerow(
                [rep.worker, rep.description, rep.arrival, rep.departure,
                 rep.productive_time,
                 rep.type_of_work, rep.project, rep.creat_time,
                 rep.edit_time, ])

    return responce


@login_required(login_url='login-AC')
@allowed_users(allowed_groups={'admin', 'worker'})
def export_to_pdf(request):
    responce = HttpResponse(content_type='application/pdf')
    responce['Content-Disposition'] = 'attachment; filename=Work_Report-' + \
                                      str(timezone.now()) + '.pdf'
    responce['Content-Transfer-Encoding'] = 'binary'

    data = models.WorkReport.objects.all()
    if request.method == "GET":
        work_report_filter = filters.WorkReportsFilter(request.GET,
                                                       queryset=data)
        data = work_report_filter.qs

    html_string = render_to_string('pdf_template.html',
                                   {'reports': data, 'total': 0})
    html = HTML(string=html_string)

    res = html.write_pdf()

    with tempfile.NamedTemporaryFile() as output:
        output.write(res)
        output.flush()

        output = open(output.name, 'rb')
        responce.write(output.read())

    return responce


def get_basic_data_for_dashboard(reports):
    def get_data(reports):
        this_month = django.utils.timezone.now().month
        data = dict()
        data['pocet_reportu'] = reports.count()
        data['pocet_hodin'] = reports.aggregate(Sum('productive_time'))

        data['pocet_reportu_tento_mesic'] = \
            reports. \
                filter(arrival__month=this_month). \
                count()
        data['pocet_hodin_tento_mesic'] = \
            reports. \
                filter(arrival__month=this_month) \
                .aggregate(Sum('productive_time'))

        data['pocet_reportu_mesic_minuly'] = \
            reports. \
                filter(arrival__month=this_month - 1). \
                count()
        data['pocet_hodin_mesic_minuly'] = \
            reports. \
                filter(arrival__month=this_month - 1) \
                .aggregate(Sum('productive_time'))
        return data

    def get_project_table(reports):
        project = reports. \
            select_related('project'). \
            values('project__name', 'project__pk'). \
            annotate(sum=Sum('productive_time')). \
            order_by('sum')
        return project

    def get_type_of_work_table(reports):
        type_of_work = reports. \
            select_related('type_of_work'). \
            values('type_of_work__label', 'type_of_work__pk'). \
            annotate(sum=Sum('productive_time')). \
            order_by('sum')
        return type_of_work

    def get_charts(reports):
        def get_chart_projects(reports):
            projects = get_project_table(reports)
            data_for_plot_cake = dict()
            for i in projects:
                data_for_plot_cake[i['project__name']] = i['sum'].total_seconds()
            project_plot = get_plot_cake(
                    name=None,
                    **data_for_plot_cake)
            return project_plot

        def get_chart_year(reports):
            start_of_month_last_year = timezone. \
                                           now(). \
                                           replace(hour=0, minute=0,
                                                   second=0,
                                                   microsecond=0) \
                                       - relativedelta(months=12)
            dates = [
                (start_of_month_last_year + relativedelta(months=i))
                for i in range(13)]

            data_for_plot_normal = dict()
            for i in get_project_table(reports):
                l = []
                for d in dates:
                    tmp = reports.select_related('project').values(
                            'project__name', 'project__pk', 'arrival')
                    tmp = tmp.filter(project__pk=i['project__pk'])
                    tmp = tmp.filter(arrival__gte=d)
                    tmp = tmp.filter(arrival__lt=(
                            d + relativedelta(
                            months=1)))
                    tmp = tmp.annotate(sum=Sum('productive_time'))
                    if len(tmp) != 0:
                        l.append(tmp[0]['sum'].seconds)
                    else:
                        l.append(0)

                data_for_plot_normal[i['project__name']] = l.copy()

            normal_plot = get_plot_normal(dates, name=None,
                                          **data_for_plot_normal)
            return normal_plot

        return get_chart_projects(reports), get_chart_year(reports)

    return get_data(reports), get_project_table(reports), \
           get_type_of_work_table(reports), get_charts(reports)


@login_required(login_url='login-AC')
@allowed_users(allowed_groups={'admin', 'worker'})
def dashboard(request):
    reports = models.WorkReport.objects.filter(worker=request.user.pk)

    data = get_basic_data_for_dashboard(reports)

    context = {'title': 'Dash Board',
               'data': data[0],
               'project': data[1],
               'type_of_work': data[2],
               'project_plot_1': data[3][0],
               'project_plot_2': data[3][1]}
    return render(request, 'work_report/dashboard.html', context)


@login_required(login_url='login-AC')
@allowed_users(allowed_groups={'admin', 'worker'})
def report_view(request):
    reports = models.WorkReport.objects.all()

    if request.method == 'GET':
        work_report_filter = filters.WorkReportsFilter(request.GET,
                                                       queryset=reports)
        reports = work_report_filter.qs

    context = {'reports': reports,
               'filter': work_report_filter,
               'title': 'Přehled',
               'has_filter': True,
               }

    return render(request, 'work_report/reports.html', context)


@login_required(login_url='login-AC')
@allowed_users(allowed_groups={'admin', 'worker'})
def project_view(request):
    projects = models.WorkReport.objects \
        .select_related('project', 'type_of_work') \
        .values('project__name', 'type_of_work__label', 'project__pk') \
        .annotate(productive_time=Sum('productive_time')) \
        .order_by('-project__pk', 'type_of_work__label')

    context = {
        'projects': projects,
        'title': 'Projekty',
        'has_filter': False,
        }

    return render(request, 'work_report/projects.html', context)


@login_required(login_url='login-AC')
@allowed_users(allowed_groups={'admin', 'worker'})
@allow_submit_own_data_post(super_user_groups={'admin'})
def create_new_report(request):
    user = request.user
    form = forms.NewWorkReportForm(initial={'worker': user})

    if request.method == 'POST':
        form = forms.NewWorkReportForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('report_list-WR'))

    context = {'form': form, 'title': 'Přidat nový záznam', }
    return render(request, 'work_report/new_report_form.html', context)


@login_required(login_url='login-AC')
@allowed_users(allowed_groups={'admin', 'worker'})
def create_new_project(request):
    form = forms.NewProjectForm()

    if request.method == 'POST':
        form = forms.NewProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('report_list-WR'))

    context = {'form': form, 'title': 'Přidat nový Project', }
    return render(request, 'work_report/new_project_form.html', context)


@login_required(login_url='login-AC')
@allowed_users(allowed_groups={'admin', 'worker'})
@allow_edit_own_data_page(super_user_groups={'admin'})
@allow_submit_own_data_post(super_user_groups={'admin'})
def edit_report(request, pk):
    report = models.WorkReport.objects.get(id=pk)
    form = forms.NewWorkReportForm(instance=report)

    if request.method == 'POST':
        logging.info('Post request:', request.POST)
        form = forms.NewWorkReportForm(request.POST, instance=report)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('report_list-WR'))

    context = {'form': form, 'title': 'Editovat záznam', }
    return render(request, 'work_report/new_report_form.html', context)


@login_required(login_url='login-AC')
@allowed_users(allowed_groups={'admin', 'worker'})
def copy_report(request, pk):
    report = models.WorkReport.objects.get(id=pk)
    form = forms.NewWorkReportForm(instance=report)

    if request.method == 'POST':
        logging.info('Post request:', request.POST)
        form = forms.NewWorkReportForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('report_list-WR')

    context = {'form': form, 'title': 'Nový záznam', }
    return render(request, 'work_report/new_report_form.html', context)


@login_required(login_url='login-AC')
@allowed_users(allowed_groups={'admin', 'worker'})
@allow_edit_own_data_page(super_user_groups={'admin'})
def delete_report(request, pk):
    report = models.WorkReport.objects.get(id=pk)
    if request.method == 'POST':
        report.delete()
        return redirect('report_list-WR')

    context = {'report': report, 'title': 'Opravdu smazat záznam',}
    return render(request, 'work_report/delete.html', context)
