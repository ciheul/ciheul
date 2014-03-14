from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from ciheul.common import MainResource, b64save_images
from jendela24 import models


class RssNewsResource(MainResource, ModelResource):
    """Resource: /jendela24/1.0/news/"""

    class Meta:
        queryset = models.RssNews.objects.order_by('published_at').reverse()
        resource_name = 'news'
        include_resource_uri = False
        excludes = ['id']
        authorization = Authorization()

    def dehydrate(self, bundle):
        #bundle.data['summary'].replace('src', 'ng-src')
        print bundle.data['summary']
        print

        return bundle
