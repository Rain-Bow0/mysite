from django.contrib import admin
from .models import LikeRecord,LikeCount
# Register your models here.


@admin.register(LikeRecord)
class LikeRecordAdmin(admin.ModelAdmin):
    list_display = ['id', 'content_type', 'object_id', 'user', 'like_time']


@admin.register(LikeCount)
class LikeCountAdmin(admin.ModelAdmin):
    list_display = ['id', 'content_type', 'object_id', 'like_num']
