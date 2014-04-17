from django.conf.urls import url
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse

from tastypie.authorization import Authorization, DjangoAuthorization
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.exceptions import TastypieError, ImmediateHttpResponse
from tastypie.http import HttpBadRequest, HttpAccepted, HttpCreated
from tastypie.paginator import Paginator
from tastypie.resources import ModelResource
from tastypie.utils import trailing_slash
from tastypie import fields

from authentication import OAuth20Authentication
from ciheul.common import MainResource, b64save_images, get_current_session
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
        """GET Method"""
        
        if not bundle.request.COOKIES['sessionid']:
            return bundle

        try:
            s = get_current_session(bundle.request.COOKIES['sessionid'])
            if s is None:
                return bundle
            activity = Activities.objects.get(user_id=s['_auth_user_id'], \
                article_id=bundle.obj.id)
            bundle.data['activity'] = {
                'read': activity.like or activity.share,
                'like': activity.like,
                'share': activity.share
            }
        except ObjectDoesNotExist:
            bundle.data['activity'] = {'read': 0, 'like': 0, 'share': 0}

        return bundle

    def hydrate(self, bundle):
        return bundle

    def prepend_urls(self):
        return [
            # GET likes
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/likes%s$" % \
                (self._meta.resource_name, trailing_slash()), \
                self.wrap_view('get_likes'), name="api_get_likes"),

            # POST read 
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/read%s$" % \
                (self._meta.resource_name, trailing_slash()), \
                self.wrap_view('post_read'), name="api_post_read"),

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

    def post_read(self, request, **kwargs):
        """
        POST /news/<news_id>/read
        """
        try:
            s = Session.objects.get(pk=request.COOKIES['sessionid']).get_decoded()
            a = Activities.objects.filter(user_id=s['_auth_user_id'], article_id=kwargs['pk'])
            if not a:
                Activities.objects.create(user_id=s['_auth_user_id'], article_id=kwargs['pk'], like=False, share=False)
            else:
                return HttpAccepted()
        except ObjectDoesNotExist:
            return Http404() 
            #raise BadRequest('Session or Activitiy does not exist.')
        except Exception:
            print "guest"
            # TODO http status does not work properly
            return Http404() 
        return HttpCreated()

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
            Activities.objects.create(user_id=s['_auth_user_id'], article_id=kwargs['pk'], like=True, share=False)
            #raise BadRequest('Session or Activitiy does not exist.')
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


class UserResource(MainResource, ModelResource):
    #activities = fields.ToManyField('ciheul.jendela24.api.ActivitiesResource', attribute='activity', full=True)

    class Meta:
        queryset = User.objects.all()
        authorization = DjangoAuthorization()
        #authentication = OAuth20Authentication()
        excludes = ['password', 'is_active', 'is_staff', 'is_superuser', 
            'resource_uri']
        resource_name = 'users'

    def dehydrate(self, bundle):
        print 'dehydrate'
        return bundle

    def hydrate(self, bundle):
        print 'hydrate'
        #raise ImmediateHttpResponse(response=HttpAccepted("debugging bro!\n"))
        return bundle

    def alter_list_data_to_serialize(self, request, response):
        print "alter_list_data_to_serialize"
        return response

    def alter_detail_data_to_serialize(self, request, response):
        print "alter_detail_data_to_serialize"
        return response

    def prepend_urls(self):
        return [
            # GET reads 
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/reads%s$" % \
                (self._meta.resource_name, trailing_slash()), \
                self.wrap_view('get_reads'), name="user_get_reads"),

            # GET likes
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/likes%s$" % \
                (self._meta.resource_name, trailing_slash()), \
                self.wrap_view('get_likes'), name="user_get_likes"),

            # GET shares 
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/shares%s$" % \
                (self._meta.resource_name, trailing_slash()), \
                self.wrap_view('get_shares'), name="user_get_shares"),
        ]

    def get_reads(self, request, **kwargs):
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
        return activities_resource.get_list(request, user=obj.pk)

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
        return activities_resource.get_list(request, user=obj.pk, like=True)

    def get_shares(self, request, **kwargs):
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
        return activities_resource.get_list(request, user=obj.pk, share=True)

class ActivitiesResource(MainResource, ModelResource):
    user = fields.ToOneField(UserResource, 'user')
    article = fields.ToOneField(RssNewsResource, 'article', full=True)
    
    class Meta:
        queryset = Activities.objects.all().order_by('article').reverse()
        authorization = DjangoAuthorization()
        resource_name = 'activities'
        include_resource_uri = False
        #excludes = ['id']
        filtering = {
            'user': ALL,        
            'article': ALL,
            'like': ALL,
            'share': ALL,
        }
        ordering = []


# http://django-tastypie.readthedocs.org/en/latest/cookbook.html
# http://stackoverflow.com/questions/14085865/exposing-model-method-with-tastypie
