from django.db import models


class RssNews(models.Model):
    title = models.CharField(max_length=150, unique=True)
    source = models.CharField(max_length=50, null=True)
    url = models.URLField(unique=True)
    summary = models.TextField()
    created_at = models.DateTimeField(auto_now=True, auto_now_add=True)
    published_at = models.DateTimeField()


class User(models.Model):
    pass
