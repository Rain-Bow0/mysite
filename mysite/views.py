from django.shortcuts import render, get_object_or_404
from django.contrib.contenttypes.models import ContentType
from read_statistics import utils
from blog.models import Blog
from django.core.cache import cache

def home(request):
    context = {}
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates, read_num = utils.get_seven_days_read_data(blog_content_type)
    seven_days_ago_hot_blogs = cache.get('seven_days_ago_hot_blogs')
    if seven_days_ago_hot_blogs is None:
        seven_days_ago_hot_blogs = utils.get_seven_days_hot_blog()
        cache.set('seven_days_ago_hot_blogs', seven_days_ago_hot_blogs, 3600)

    context['dates'] = dates
    context['read_num'] = read_num
    context['today_hot_blog'] = utils.get_today_hot_blog(blog_content_type)
    context['yesterday_hot_blog'] = utils.get_yesterday_hot_blog()
    context['seven_days_ago_hot_blogs'] = seven_days_ago_hot_blogs
    return render(request, 'home.html', context)
