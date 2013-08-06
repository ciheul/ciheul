from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from ciheul.common import MainResource
from bigear import models


class ReportResource(MainResource, ModelResource):
    class Meta:
        queryset = models.Report.objects.all()
        resource_name = 'report'
        include_resource_uri = False
        excludes = ['id']
        authorization = Authorization()


#class TweetResource(MainResource, ModelResource):
#    class Meta:
#        queryset = models.Tweet.objects.all()
#        resource_name = 'tweet'
#        include_resource_uri = False
#        excludes = ['id']
