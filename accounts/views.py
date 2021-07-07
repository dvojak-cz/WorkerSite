from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from work_report.decorators import unauthenticated_user


@unauthenticated_user
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard-WR')
        else:
            messages.info(request, 'Zadal jste špatné heslo')

    context = {}
    return render(request, 'login/login.html', context)


@login_required(login_url='login-AC')
def logout_page(request):
    logout(request)
    return redirect('login-AC')
