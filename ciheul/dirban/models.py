from django.db import models


class Business(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=200)
    business_type = models.CharField(max_length=20)
    longitude = models.FloatField(max_length=20)
    latitude = models.FloatField(max_length=20)
    contributor = models.CharField(max_length=30)

    def __unicode__(self):
        return u'%s => %s' % (self.name, self.business_type)
