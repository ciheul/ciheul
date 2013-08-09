from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from ciheul.common import MainResource
from bigear import models


class ReportResource(MainResource, ModelResource):
    #image = fields.FileField(attribute='imageupload')

    class Meta:
        queryset = models.Report.objects.all()
        list_allow_methods = ['get', 'post']
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
