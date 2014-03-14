from django.db import models


class RssNews(models.Model):
    title = models.CharField(max_length=150, unique=True)
    url = models.URLField(unique=True)
    summary = models.TextField()
    created_at = models.DateTimeField(auto_now=True, auto_now_add=True)
    published_at = models.DateTimeField()
