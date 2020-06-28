from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import auth
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from read_statistics import utils
from blog.models import Blog



# 使用缓存，通过方法名来进行调用，减少重复代码
def use_cache(hot_blog):
    hot_blog_data = cache.get(hot_blog)
    if hot_blog_data is None:
        hot_blog_data = eval('utils.get_'+hot_blog)()
        cache.set(hot_blog, hot_blog_data, 3600)
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
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(request, username=username, password=password)
    if user is None:
        return render(request, 'error.html', {'message': '用户名或密码不正确'})
    else:
        auth.login(request, user)
        return redirect('/')