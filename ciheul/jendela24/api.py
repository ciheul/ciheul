from django.conf.urls import url
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse

from tastypie.authorization import Authorization, DjangoAuthorization
from tastypie.exceptions import TastypieError, ImmediateHttpResponse
from tastypie.http import HttpBadRequest, HttpAccepted, HttpCreated
from tastypie.paginator import Paginator
from tastypie.resources import ModelResource
from tastypie.utils import trailing_slash

from authentication import OAuth20Authentication
from ciheul.common import MainResource, b64save_images
from jendela24.models import Activities, RssNews


class RssNewsResource(MainResource, ModelResource):
#class RssNewsResource(ModelResource):
    """Resource: /jendela24/1.0/news/"""

    class Meta:
        queryset = RssNews.objects.all().order_by('published_at').reverse()
        resource_name = 'news'
        include_resource_uri = False
        #excludes = ['id']
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

    def prepend_urls(self):
        return [
            # GET likes
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/likes%s$" % \
                (self._meta.resource_name, trailing_slash()), \
                self.wrap_view('get_likes'), name="api_get_likes"),

            # POST like
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/like%s$" % \
                (self._meta.resource_name, trailing_slash()), \
                self.wrap_view('post_like'), name="api_post_like"),

            # POST unlike
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/unlike%s$" % \
                (self._meta.resource_name, trailing_slash()), \
                self.wrap_view('post_unlike'), name="api_post_unlike"),

            # POST share 
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/share%s$" % \
                (self._meta.resource_name, trailing_slash()), \
                self.wrap_view('post_share'), name="api_post_share"),
        ]

    def get_likes(self, request, **kwargs):
        try:
            bundle = self.build_bundle(data={'pk': kwargs['pk']}, \
                request=request)
            obj = self.cached_obj_get(bundle=bundle, \
                **self.remove_api_resource_names(kwargs))
        except ObjectDoesNotExist:
            return HttpGone()
        except MultipleObjectsReturned:
            return HttpMultipleChoices("More than one resource is found at this URI")

        activities_resource = ActivitiesResource()
        #return activities_resource.get_list(request)
        return activities_resource.get_detail(request, article_id=obj.pk)

    def post_like(self, request, **kwargs):
        """
        POST /news/<news_id>/like
        """
        try:
            s = Session.objects.get(pk=request.COOKIES['sessionid']).get_decoded()
            activity = Activities.objects.get(user_id=s['_auth_user_id'], article_id=kwargs['pk'])
            activity.like = True
            activity.save()
        except ObjectDoesNotExist:
            raise BadRequest('Session or Activitiy does not exist.')
        except Exception:
            print "guest"
            # TODO http status does not work properly
            return Http404() 
        return HttpCreated()

    def post_unlike(self, request, **kwargs):
        """
        POST /news/<news_id>/unlike
        """
        try:
            s = Session.objects.get(pk=request.COOKIES['sessionid']).get_decoded()
            activity = Activities.objects.get(user_id=s['_auth_user_id'], article_id=kwargs['pk'])
            activity.like = False
            activity.save()
        except ObjectDoesNotExist:
            raise BadRequest('Activitiy does not exist.')
        return HttpCreated()

    def post_share(self, request, **kwargs):
        """
        POST /news/<news_id>/share
        """
        try:
            s = Session.objects.get(pk=request.COOKIES['sessionid']).get_decoded()
            activity = Activities.objects.get(user_id=s['_auth_user_id'], article_id=kwargs['pk'])
            activity.share = True
            activity.save()
        except ObjectDoesNotExist:
            raise BadRequest('Activitiy does not exist.')
        return HttpCreated()


class ActivitiesResource(MainResource, ModelResource):
    class Meta:
        queryset = Activities.objects.all()
        authorization = Authorization()
        resource_name = 'activities'
        include_resource_uri = False
        excludes = ['id']

    #def get_detail(self, request, **kwargs):
    #    print 'get_detail 1'
    #    try:
    #        bundle = self.build_bundle(data={'id': kwargs['id']}, \
    #            request=request)
    #        print bundle.data
    #    except ObjectDoesNotExist:
    #        return HttpGone()
    #    print 'get_detail 3'
    #    return bundle


class UserResource(MainResource, ModelResource):
    class Meta:
        queryset = User.objects.all()
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



# http://django-tastypie.readthedocs.org/en/latest/cookbook.html
# http://stackoverflow.com/questions/14085865/exposing-model-method-with-tastypie
