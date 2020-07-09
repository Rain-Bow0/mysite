from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User

from django.urls import reverse

from .forms import LoginForm, RegisterForm
from django.http import JsonResponse


def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            auth.login(request, login_form.cleaned_data['user'])
            return redirect(request.GET.get('from', reverse('home')))
    else:
        login_form = LoginForm()

    content = {}
    content['login_form'] = login_form
    return render(request, 'login.html', content)


def login_for_modal(request):
    login_form = LoginForm(request.POST)
    data = {}
    if login_form.is_valid():
        auth.login(request, login_form.cleaned_data['user'])
        data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)


def register(request):
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            email = register_form.cleaned_data['email']
            password = register_form.cleaned_data['password']
            user = User.objects.create_user(username, email, password)
            user.save()
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('home')))
    else:
        register_form = RegisterForm()

    content = {}
    content['register_form'] = register_form
    return render(request, 'register.html', content)


def logout(request):
    auth.logout(request)
    return redirect(request.GET.get('from', reverse('home')))


def user_info(request):
    return render(request, 'user_info.html')
