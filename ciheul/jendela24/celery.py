from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings
from redis import StrictRedis
import time
import feedparser


# set the default Django settings module for the 'celery' program
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ciheul.settings')

app = Celery('ciheul')
redis = StrictRedis('localhost')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print "Request: {0!r}".format(self.request)


@app.task
def publish_news():
    print "publish_news"
    time.sleep(5)
    for i in range(0, 20):
        msg = 'Task message %s\n' % i
        print "msg:" + msg
        redis.publish("news_from_redis", msg)
        time.sleep(0.1)


@app.task
def fetch_rss():
    #rss_url = 'http://rss.kontan.co.id/v2/investasi'
    #rss = feedparser.parse(rss_url)
    #rss = ['xxx', 'yyy', 'zzz']
    #k = 1
    #v = 'hello'
    for r in rss:
       redis.rpush('kontan', r)
    #    redis.zadd()
    #rss = {'x': 1}
    print k, v 
    #return k, v
