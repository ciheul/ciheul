from tastypie.exceptions import TastypieError, ImmediateHttpResponse
from tastypie.http import HttpBadRequest, HttpAccepted
from tastypie.resources import ModelResource
from tastypie.authorization import Authorization, DjangoAuthorization
from authentication import OAuth20Authentication
from tastypie.paginator import Paginator
from ciheul.common import MainResource, b64save_images
from jendela24 import models
from django.http import HttpResponse


#class CustomBadRequest(TastypieError):
#    def __init__(self, code="", message=""):
#        self._response = {
#            "error": {"code": code or "not_provided",
#                      "message": message or "not_provided"}
#        }
#
#    @property
#    def response(self):
#        print "CustomBadRequest.response()"
#        return HttpBadRequest(
#            json.dumps(self._response),
#            content_type='application/json')


class RssNewsResource(MainResource, ModelResource):
#class RssNewsResource(ModelResource):
    """Resource: /jendela24/1.0/news/"""

    class Meta:
        queryset = models.RssNews.objects.all().order_by('published_at').reverse()
        resource_name = 'news'
        include_resource_uri = False
        excludes = ['id']
        authorization = Authorization()
        #paginator_class = Paginator

    def dehydrate(self, bundle):
        #print bundle.request.GET['limit']
        #print bundle.request.GET['q']
        return bundle

    def hydrate(self, bundle):
        print "1: ", bundle.request.GET['limit']
        #print "2: ", bundle.request.GET['q']
        #print "3: ", bundle.data['limit']
        #print "4: ", bundle.data['x']
        #print "5: ", bundle.obj
        return bundle


class UserResource(MainResource, ModelResource):
    class Meta:
        queryset = models.User.objects.all()
        authorization = DjangoAuthorization()
        authentication = OAuth20Authentication()
        resource_name = 'user'

    def dehydrate(self, bundle):
        print "dehydrate"
        #print bundle.request
        return bundle

    def hydrate(self, bundle):
        print "hydrate"
        print bundle.request.user
        print bundle.request.user.is_authenticated()
        print bundle.request.user.is_active
        print bundle.request.POST
        

        raise ImmediateHttpResponse(response=HttpAccepted("debugging bro!\n"))
        return bundle

    def alter_list_data_to_serialize(self, request, response):
        print "alter_list_data_to_serialize"
        return response

    def alter_detail_data_to_serialize(self, request, response):
        print "alter_detail_data_to_serialize"
        return response

    #def obj_get(self, request):
    #    print "obj_get"
