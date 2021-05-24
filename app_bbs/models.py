from django.conf import settings
from django.db import models
from django.utils import timezone


class Post(models.Model):
    author = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def unpublish(self):
        self.published_date = None
        self.save()

    def allowed_comments(self):
        return self.comments.filter(is_excluded=False)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey('app_bbs.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    is_excluded = models.BooleanField(default=False)

    def allow(self):
        self.is_excluded = False
        self.save()

    def exclude(self):
        self.is_excluded = True
        self.save()

    def __str__(self):
        return self.text
