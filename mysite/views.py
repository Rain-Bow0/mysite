from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django.urls import reverse
from read_statistics import utils
from blog.models import Blog
from .forms import LoginForm, RegisterForm


# 使用缓存，通过方法名来进行调用，减少重复代码
def use_cache(hot_blog):
    hot_blog_data = cache.get(hot_blog)
    if hot_blog_data is None:
        hot_blog_data = eval('utils.get_'+hot_blog)()
        cache.set(hot_blog, hot_blog_data, 60)
    return hot_blog_data


def home(request):
    context = {}
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates, read_num = utils.get_seven_days_read_data(blog_content_type)

    context['dates'] = dates
    context['read_num'] = read_num
    context['today_hot_blog'] = use_cache('today_hot_blog')
    context['yesterday_hot_blog'] = use_cache('yesterday_hot_blog')
    context['seven_days_ago_hot_blog'] = use_cache('seven_days_ago_hot_blog')
    return render(request, 'home.html', context)


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
