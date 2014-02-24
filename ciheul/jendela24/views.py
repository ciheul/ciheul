from celery import Celery
from django.shortcuts import render
from django.http import HttpResponse
from socketio import socketio_manage
from socketio.namespace import BaseNamespace
from redis import StrictRedis
from .celery import publish_news
import time

redis = StrictRedis('localhost')


def home(request):
    context = {
        'title_head': 'Jendela24',
        'title': 'Jendela24',
    }
    q = request.GET.get('q', '')
    if q:
        print 'q:', q
        publish_news.delay()
    return render(request, "jendela24/base_jendela24.html", context)


def socketio(request):
    print "socketio"
    socketio_manage(request.environ, {
        '/jendela24/news': NewsNamespace
    })
    return HttpResponse()


class NewsNamespace(BaseNamespace):
    def on_subscribe(self):
        print "on_subscribe"
        self.sub = redis.pubsub()
        self.spawn(self.listen)

    def listen(self):
        print "listen"
        self.sub.subscribe("news_from_redis")
        for news in self.sub.listen():
            print "news:", news
            if news['type']  == 'message':
                self.emit('news_via_socketio', news['data'])