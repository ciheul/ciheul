from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from socketio import socketio_manage
from socketio.namespace import BaseNamespace
from social.backends.twitter import TwitterOAuth
from redis import StrictRedis
from celery import Celery
from .celery import publish_news
import time
import json
import os.path


redis = StrictRedis('localhost')


def show_color(request):
    if 'favorite_color' in request.COOKIES:
        return HttpResponse("Your favorite color is %s" % \
            request.COOKIES["favorite_color"])
    return HttpResponse("You don't have a favorite color.")


def set_color(request):
    if 'favorite_color' in request.GET:
        response = HttpResponse("Your favorite color is now %s" % \
            request.GET['favorite_color'])
        response.set_cookie('favorite_color', request.GET['favorite_color'])
        return response
    else:
        return HttpResponse("You didn't give a favorite color.")


def about(request):
    if request.session.test_cookie_worked():
        #request.session.delete_test_cookie()
        return HttpResponse("the test cookie works!")
    return HttpResponse("cookie fails.")


def home(request):
    print "home"
    #if getattr(request.session['username'], None):
    try:
        username = request.session['username']
        print 'jendela24. username:', username
    except KeyError:
        username = 'guest'
        print "no username in session"

    context = {
        'title': 'Jendela24',
        'twitter_id': getattr(settings, 'SOCIAL_AUTH_TWITTER_KEY', None),
        'username': username
    }
    return render(request, os.path.join(settings.DJANGO_ROOT, '../angular-seed/jendela24/index.html'), context)


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

        print 'listening...'

        for news in self.sub.listen():
            if news['type'] == 'message':
                message = json.loads(news['data'])
                if message == 'init': continue
                print message
                self.emit('news_via_socketio', json.dumps(message))

    def listen(self):
        print "listen"
        self.sub.subscribe("news_from_redis")
        for news in self.sub.listen():
            print "news:", news
            if news['type']  == 'message':
                self.emit('news_via_socketio', news['data'])
