from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings
from redis import Redis
import time
from datetime import datetime
from time import mktime
import feedparser
import psycopg2
import rfc822


# set the default Django settings module for the 'celery' program
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ciheul.settings')

app = Celery('ciheul')
redis = Redis('localhost')

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
    conn_string = "host='localhost' dbname='ciheul' user='winnuayi' password=''"
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    print "Connected to database!\n"
    
    rss_list = open('ciheul/jendela24/rss_list.txt', 'r')
    for rss in rss_list:
        # ignore commented line
        if rss.startswith('#'): continue

        feed = feedparser.parse(rss)
        print rss
        print
        #feed = feedparser.parse(r'bandung-raya')
        for f in feed['entries']:
            # ignore mobile link
            if filter_mobile_url(f['links']): continue

            print f['link']
            # sql insert. only unique news is inserted. not Django-way
            insert_string = """
                INSERT INTO jendela24_rssnews 
                    (title, url, summary, created_at, published_at)
                    SELECT %s, %s, %s, %s, %s
                    WHERE NOT EXISTS (SELECT 1 FROM jendela24_rssnews WHERE url=%s)
            """
        
            # insert rss news to database
            cursor.execute(insert_string, 
                    (f['title'], f['link'], f['summary'], datetime.now(), 
                    convert_pub_date(f['published']), f['link']))
            conn.commit()
        
            # info
            #print f['title']
        print "=========================="
    
    conn.close()


def filter_mobile_url(url):
    if 'm.detik.com' in url:
        return True
    return False


def convert_time(t):
    """Convert from time format to datetime format."""
    return datetime.fromtimestamp(mktime(t))


def convert_pub_date(str_t):
    """Convert from pubDate (RFC822) format to datetime format."""
    return datetime.fromtimestamp(rfc822.mktime_tz(rfc822.parsedate_tz(str_t)))


#@app.task
#def fetch_rss():
#    #rss_url = 'http://rss.kontan.co.id/v2/investasi'
#    #rss = feedparser.parse(rss_url)
#    #rss = ['xxx', 'yyy', 'zzz']
#    #k = 1
#    #v = 'hello'
#    for r in rss:
#       redis.rpush('kontan', r)
#    #    redis.zadd()
#    #rss = {'x': 1}
#    print k, v 
#    #return k, v


