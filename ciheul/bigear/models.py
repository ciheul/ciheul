from django.db import models


class Report(models.Model):
    name = models.CharField(max_length=20)
    screen_name = models.CharField(max_length=20)
    text = models.CharField(max_length=160)
    profile_image_url = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now=True, auto_now_add=True)
    is_like = models.BooleanField(default=False)
    num_likes = models.IntegerField(default=0)
    #image = models.ImageField(upload_to="static/img/", null=True, blank=True)
    #geolocation isn't implemented

    def __unicode__(self):
        return u'%s => %s' % (self.name, self.text)


#class Tweet(models.Model):
#    id_str = models.CharField(max_length=20)
#    name = models.CharField(max_length=20)
#    screen_name = models.CharField(max_length=20)
#    profile_image_url = models.CharField(max_length=100)
#    created_at = models.CharField(max_length=30)
#    text = models.CharField(max_length=160)
#
#    def __unicode__(self):
#        return u'%s => %s' % (self.screen_name, self.text)
