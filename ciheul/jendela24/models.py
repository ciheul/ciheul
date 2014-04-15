from django.db import models
from django.contrib.auth.models import User


class RssNews(models.Model):
    title = models.CharField(max_length=150, unique=True)
    source = models.CharField(max_length=50, null=True)
    url = models.URLField(unique=True)
    summary = models.TextField()
    created_at = models.DateTimeField(auto_now=True, auto_now_add=True)
    published_at = models.DateTimeField()
    user = models.ManyToManyField(User, through='Activities')

    def __unicode__(self):
        return self.title


class Activities(models.Model):
    user = models.ForeignKey(User)
    article = models.ForeignKey(RssNews)
    like = models.BooleanField()
    share = models.BooleanField()

    def __unicode__(self):
        return u'%s -> %s' % (self.user.id, self.article.id)
