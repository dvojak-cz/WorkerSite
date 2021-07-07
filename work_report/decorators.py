from django.http import HttpRequest
from django.shortcuts import redirect

from .models import WorkReport


def unauthenticated_user(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard-WR')
        return func(request, *args, **kwargs)

    return wrapper


def allowed_users(*, allowed_groups=None, ):
    if allowed_groups is None:
        allowed_groups = list()

    def inner(func):
        def wrapper(request, *args, **kwargs):
            if len({gr.name for gr in request.user.groups.all()}.intersection(
                    allowed_groups)) != 0:
                return func(request, *args, **kwargs)
            else:
                return redirect('unauthorised-AR')

        return wrapper

    return inner


def allow_edit_own_data_page(*, super_user_groups=None):
    if super_user_groups is None:
        super_user_groups = list()

    def inner(func):
        def wrapper(request: HttpRequest, pk, *args, **kwargs):
            if (request.user.id == WorkReport.objects.get(pk=pk).worker.id) \
                    or (len({gr.name for gr in request.user.groups.all()}
                                    .intersection(super_user_groups)) != 0):
                return func(request, pk, *args, **kwargs)
            else:
                return redirect('unauthorised-AR')

        return wrapper

    return inner


def allow_submit_own_data_post(*, super_user_groups=None):
    if super_user_groups is None:
        super_user_groups = list()

    def inner(func):
        def wrapper(request: HttpRequest, *args, **kwargs):
            if request.method == 'POST':
                if (str(request.user.id) == request.POST["worker"]) or (
                        len({gr.name for gr in
                             request.user.groups.all()}.intersection(
                                super_user_groups)) != 0):
                    return func(request, *args, **kwargs)
                else:
                    return redirect('unauthorised-AR')
            return func(request, *args, **kwargs)

        return wrapper

    return inner
