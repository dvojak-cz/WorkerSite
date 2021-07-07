from datetime import datetime, date

import dateutil.relativedelta
from django import template

register = template.Library()


@register.filter
def duration(td):
    if isinstance(td, str):
        return td
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60

    return '{}h {}m'.format(hours, minutes)


@register.simple_tag(takes_context=False)
def current_year_filter():
    start_of_current_year = \
        date(datetime.today().year, 1, 1)
    return f'?worker=&project=&type_of_work=&start=' \
           f'{start_of_current_year}T12%3A00&end='


@register.simple_tag(takes_context=False)
def last_year_filter():
    start_of_current_year = \
        date(datetime.today().year, 1, 1)
    start_of_last_year = \
        start_of_current_year - dateutil.relativedelta.relativedelta(year=1)
    return f'?worker=&project=&type_of_work=&start=' \
           f'{start_of_last_year}T12%3A00&end={start_of_current_year}T12%3A00'


@register.simple_tag(takes_context=False)
def current_month_filter():
    start_of_current_month = \
        date(datetime.today().year, datetime.today().month, 1)
    return f'?worker=&project=&type_of_work=&start=' \
           f'{start_of_current_month}T12%3A00&end='


@register.simple_tag(takes_context=False)
def last_month_filter():
    start_of_current_month = \
        date(datetime.today().year, datetime.today().month, 1)
    start_of_last_month = \
        start_of_current_month - dateutil.relativedelta.relativedelta(months=1)
    return f'?worker=&project=&type_of_work=&start=' \
           f'{start_of_last_month}T12%3A00&end=' \
           f'{start_of_current_month}T12%3A00'
