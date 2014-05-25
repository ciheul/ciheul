from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    description = models.CharField(max_length=150, default='')
    homepage = models.URLField(default='')
    location = models.CharField(max_length=100, default='')
    profile_image_url = models.URLField(default='')
    description = models.CharField(max_length=150, default='')


class RssNews(models.Model):
    title = models.CharField(max_length=150, unique=True)
    source = models.CharField(max_length=50, null=True)
    url = models.URLField(unique=True)
    summary = models.TextField(default='')
    created_at = models.DateTimeField(auto_now=True, auto_now_add=True)
    published_at = models.DateTimeField()
    user = models.ManyToManyField(UserProfile, through='Activities')
    content = models.TextField(default='')
    image_url = models.URLField(default='')

    def __unicode__(self):
        return self.title


class Activities(models.Model):
    user = models.ForeignKey(UserProfile)
    article = models.ForeignKey(RssNews)
    like = models.BooleanField()
    dislike = models.BooleanField()
    share = models.BooleanField()

    def __unicode__(self):
        return u'%s -> %s' % (self.user.id, self.article.id)


class ArticleStat(models.Model):
    article = models.ForeignKey(RssNews)
    date = models.DateField(auto_now=True, auto_now_add=True)
    reads = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    shares = models.IntegerField(default=0)

    def __unicode__(self):
        return u'reads: %s | likes: %s | dislikes: %s | shares: %s' \
            % (self.reads, self.likes, self.dislikes, self.shares)
