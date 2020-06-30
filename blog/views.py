from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count
from django.conf import settings
from .models import Blog, BlogType
from read_statistics import utils
from comment.models import Comment
from comment.forms import CommentForm


# 传入所需要的博客，以及request，返回博客公共部分的内容，blogs， blog_type， blog_dates， blog_range
def get_blog_list_common_date(request, blog_all_list):
    page_num = request.GET.get('page', 1)
    paginator = Paginator(blog_all_list, settings.EACH_PAGE_BLOG_NUMBER)
    page_range = [i for i in range(int(page_num) - 2, int(page_num) + 3) if i in paginator.page_range]
    if page_range[0] != 1:
        if page_range[0] != 2:
            page_range.insert(0, "...")
        page_range.insert(0, 1)

    if page_range[-1] != paginator.num_pages:
        if page_range[-1] != paginator.num_pages - 1:
            page_range.append("...")
        page_range.append(paginator.num_pages)

    blog_dates = Blog.objects.dates('created_time', 'month', order='DESC')
    blog_date_dict = {}
    for date in blog_dates:
        blog_date_dict[date] = Blog.objects.filter(created_time__year=date.year, created_time__month=date.month).count()

    context = {}
    context['blogs'] = paginator.get_page(page_num)
    context['blog_dates'] = blog_date_dict
    context['page_range'] = page_range
    context['blog_types'] = BlogType.objects.annotate(blog_type_count=Count('blog'))

    return context


# Create your views here.
def blog_list(request):
    blog_all_list = Blog.objects.all()
    context = get_blog_list_common_date(request, blog_all_list)

    return render(request, template_name='blog_list.html', context=context)


def blog_detail(request, blog_pk):
    blog = get_object_or_404(Blog, pk=blog_pk)
    read_cookie_key = utils.read_statics_once_read(request, blog)

    blog_content_type = ContentType.objects.get_for_model(blog)
    comments = Comment.objects.filter(content_type=blog_content_type, object_id=blog_pk)

    context = {}
    context['blog'] = blog
    context['previous_blog'] = Blog.objects.filter(pk__lt=blog.pk).first()
    context['next_blog'] = Blog.objects.filter(pk__gt=blog.pk).last()
    context['blog_dates'] = Blog.objects.dates('created_time', 'month', order='DESC')
    context['comments'] = comments
    context['comment_form'] = CommentForm(initial={'content_type': blog_content_type.model, 'object_id': blog.pk})
    response = render(request, 'blog_detail.html', context)
    # 设置Cookie
    response.set_cookie(read_cookie_key, 'true', max_age=1200)
    return response


def blog_with_type(request, blog_type_pk):
    # 获取该分类下的博客
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    blog_all_list = Blog.objects.filter(blog_type=blog_type)

    context = get_blog_list_common_date(request, blog_all_list)
    context['blog_type'] = blog_type

    return render(request, 'blog_with_type.html', context)


def blog_with_date(request, year, month):
    blog_all_list = Blog.objects.filter(created_time__year=year, created_time__month=month)
    context = get_blog_list_common_date(request, blog_all_list)
    context['blog_with_date'] = '%s年%s月' % (year, month)

    return render(request, 'blog_with_date.html', context)
