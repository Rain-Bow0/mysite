import datetime
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models import Sum
from blog.models import Blog
from .models import ReadNum, ReadDetail


def read_statics_once_read(request, obj):
    ct = ContentType.objects.get_for_model(obj)
    key = "%s_%s_read" % (ct.model, obj.pk)
    if not request.COOKIES.get('blog_%s_read' % obj.pk):
        # 总阅读数
        readnum, create_num = ReadNum.objects.get_or_create(content_type=ct, object_id=obj.pk)
        readnum.read_num += 1
        readnum.save()

        # 当天阅读数
        readdetail, create_detail = ReadDetail.objects.get_or_create(content_type=ct, object_id=obj.pk,
                                                                     date=timezone.now().date())
        readdetail.read_num += 1
        readdetail.save()

    return key


def get_seven_days_read_data(content_type):
    today = timezone.now().date()
    read_detail_sum = []
    dates = []
    for day in range(6, -1, -1):
        date = today - datetime.timedelta(days=day)
        dates.append(date.strftime("%m/%d"))
        read_details = ReadDetail.objects.filter(content_type=content_type, date=date)
        read_sum = read_details.aggregate(read_num_sum=Sum('read_num'))
        read_detail_sum.append(read_sum['read_num_sum'] or 0)
    return dates, read_detail_sum


def get_today_hot_blog():
    # 另一种方法, 需要传入参数content_type
    # today = timezone.now().date()
    # read_details = ReadDetail.objects.filter(content_type=content_type, date=today)
    # return read_details.order_by('-read_num')[:7]  # 排序取前七条
    today = timezone.now().date()
    blogs = Blog.objects.filter(read_details__date=today) \
        .annotate(read_num=Sum('read_details__read_num')) \
        .order_by('-read_num')
    print(blogs)
    return blogs[:7]  # 排序取前七条


def get_yesterday_hot_blog():
    today = timezone.now().date()
    yesterday = today - datetime.timedelta(days=1)
    blogs = Blog.objects.filter(read_details__date=yesterday)\
                        .annotate(read_num=Sum('read_details__read_num'))\
                        .order_by('-read_num')
    return blogs[:7]  # 排序取前七条


def get_seven_days_ago_hot_blog():
    today = timezone.now().date()
    seven_days_ago = today - timezone.timedelta(days=7)
    blogs = Blog.objects.filter(read_details__date__lt=today, read_details__date__gte=seven_days_ago)\
                        .values('id', 'title')\
                        .annotate(read_num_sum=Sum('read_details__read_num'))\
                        .order_by('-read_num_sum')
    return blogs[:7]