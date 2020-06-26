from django.shortcuts import render, get_object_or_404
from django.contrib.contenttypes.models import ContentType
from read_statistics import utils
from blog.models import Blog


def home(request):
    context = {}
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates, read_num = utils.get_seven_days_read_data(blog_content_type)
    context['dates'] = dates
    context['read_num'] = read_num

    return render(request, 'home.html', context)
