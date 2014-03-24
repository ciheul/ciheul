from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from tastypie.paginator import Paginator
from ciheul.common import MainResource, b64save_images
from jendela24 import models


class RssNewsResource(MainResource, ModelResource):
#class RssNewsResource(ModelResource):
    """Resource: /jendela24/1.0/news/"""

    class Meta:
        queryset = models.RssNews.objects.all().order_by('published_at').reverse()
        #queryset = models.RssNews.objects.all()
        resource_name = 'news'
        include_resource_uri = False
        excludes = ['id']
        authorization = Authorization()
        #paginator_class = Paginator
