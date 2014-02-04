from django.db import models


class Administrative(models.Model):
    administrative_type = models.CharField(max_length=20)
    name = models.CharField(max_length=50)
    leader = models.CharField(blank=True, max_length=50)
    address = models.TextField(blank=True)
    population_male = models.IntegerField(default=0)
    population_female = models.IntegerField(default=0)
    land_area = models.FloatField(default=0)
    population_density = models.FloatField(default=0)
    email = models.EmailField(blank=True)
    telephone = models.CharField(blank=True, max_length=20)
    created_at = models.DateTimeField(auto_now=True, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def __unicode__(self):
        return u'%s %s' % (self.administrative_type, self.name)
