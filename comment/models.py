from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db import models
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import threading


# Create your models here.
class SendEmail(threading.Thread):
    def __init__(self, title, text, email):
        self.title = title
        self.text = text
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        send_mail(self.title, self.text,
                  settings.EMAIL_HOST_USER, [self.email], fail_silently=False)


class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    text = models.TextField()
    comment_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    parent = models.ForeignKey('self', related_name='parent_comment', null=True, on_delete=models.CASCADE)
    root = models.ForeignKey('self', related_name='root_comment', null=True, on_delete=models.CASCADE)
    reply_to = models.ForeignKey(User, related_name='replies', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.text

    def send_email(self):
        if self.parent is None:
            title = '有人评论了你的博客'
            email = self.user.email
        else:
            title = '有人回复了你的评论'
            email = self.reply_to.email
        if email != '':
            context = {}
            context['text'] = strip_tags(self.text)
            context['url'] = self.content_object.get_url()
            text = render_to_string('send_email.html', context=context)
            send_email = SendEmail(title, text, email)
            send_email.start()
