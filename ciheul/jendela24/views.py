from celery import Celery
from django.shortcuts import render
from django.http import HttpResponse
from socketio import socketio_manage
from socketio.namespace import BaseNamespace
from redis import StrictRedis
from .celery import publish_news
import time
import pickle

redis = StrictRedis('localhost')


def home(request):
    context = {
        'title': 'Jendela24',
        'app_css': 'jendela24.css',
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
    def initialize(self):
        print "Socketio session started"
        #self.log("Socketio session started")

    def log(self, message):
        pass
        #self.logger.info("[{0}] {1}".format(self.socket.sessid, message))

    def recv_connect(self):
        print "New connection"
        #self.log("New connection")

    def recv_disconnect(self):
        print "Disconnect"
        #self.log("Client disconnected")

    def on_subscribe(self, msg):
        print "on_subscribe"
        self.sub = redis.pubsub()
        #self.spawn(self.listen)
        self.spawn(self.listen_realtime_news)

    def listen_realtime_news(self):
        print "listen realtime news"
        self.sub.subscribe("realtime_news")
        while True:
            print 'listening...'
            for news in self.sub.listen():
                if news['type'] == 'message':
                    x = pickle.loads(news['data'])
                    if x == 'init': continue
                    print x
                    self.emit('news_via_socketio', x['title'], x['source'], x['published_at'])

    def listen(self):
        print "listen"
        self.sub.subscribe("news_from_redis")
        for news in self.sub.listen():
            print "news:", news
            if news['type']  == 'message':
                self.emit('news_via_socketio', news['data'])
