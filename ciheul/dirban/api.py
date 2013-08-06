from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from ciheul.common import MainResource
from dirban import models


class BusinessResource(MainResource, ModelResource):
    class Meta:
        queryset = models.Business.objects.all()
        resource_name = 'business'
        include_resource_uri = False
        excludes = ['id']
        authorization = Authorization()
