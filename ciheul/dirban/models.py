from django.db import models

class Business(models.Model):
    name = models.CharField(max_length=30)
    business_type = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    #lonlat
    #photos stored in another table

    def __unicode__(self):
        return u'%s => %s' % (self.name, self.business_type)
