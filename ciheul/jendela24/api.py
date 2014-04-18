from django.conf.urls import url
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, Http404

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
from jendela24.models import Activities, RssNews, UserProfile
from boilerpipe.extract import Extractor


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
        
        #print bundle.data['content']
        if bundle.data['content']:
            extractor = Extractor(extractor='ArticleExtractor', html=bundle.data['content'])
            bundle.data['content'] = extractor.getText()

        # no cookies or no sessionid field in cookies, then just send normal
        # newsfeed to anonymous user
        if not bundle.request.COOKIES or not bundle.request.COOKIES['sessionid']:
            return bundle

        try:
            # even if there is a cookie, sessionid field might be not exist,
            # then it is also anonymous user
            s = get_current_session(bundle.request.COOKIES['sessionid'])
            if s is None:
                return bundle

            # get activity information whether user has already
            # read/liked/shared
            activity = Activities.objects.get(user_id=s['_auth_user_id'], \
                article_id=bundle.obj.id)

            # assign information 
            bundle.data['activity'] = {
                'read': activity.like or activity.share,
                'like': activity.like,
                'share': activity.share
            }

        except ObjectDoesNotExist:
            # assign False if the news has never been opened
            bundle.data['activity'] = {'read': 0, 'like': 0, 'share': 0}

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

            # get userprofile from user.id
            user_profile = UserProfile.objects.get(user_id=s['_auth_user_id'])

            # check whether user has opened the article
            a = Activities.objects.filter(user_id=user_profile.id, \
                article_id=kwargs['pk'])
            if not a:
                # if not, create a new one
                Activities.objects.create(user_id=user_profile.id, \
                    article_id=kwargs['pk'], like=False, share=False)
            else:
                # just ignore
                return HttpAccepted()
        except ObjectDoesNotExist:
            return Http404() 
            #raise BadRequest('Session or Activity does not exist.')
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

            # get userprofile from user.id
            user_profile = UserProfile.objects.get(user_id=s['_auth_user_id'])

            activity = Activities.objects.get(user_id=user_profile.id, \
                article_id=kwargs['pk'])
            activity.like = True
            activity.save()
        except ObjectDoesNotExist:
            Activities.objects.create(user_id=user_profile.id, \
                article_id=kwargs['pk'], like=True, share=False)
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

            # get userprofile from user.id
            user_profile = UserProfile.objects.get(user_id=s['_auth_user_id'])

            activity = Activities.objects.get(user_id=user_profile.id, \
                article_id=kwargs['pk'])
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

            # get userprofile from user.id
            user_profile = UserProfile.objects.get(user_id=s['_auth_user_id'])

            activity = Activities.objects.get(user_id=user_profile.id, \
                article_id=kwargs['pk'])
            activity.share = True
            activity.save()
        except ObjectDoesNotExist:
            raise BadRequest('Activitiy does not exist.')
        return HttpCreated()


class UserResource(MainResource, ModelResource):
    # impossible to add fields here. we cannot add attributes to built-in
    # django model directly and tailor it with UserResource. instead, add 
    # ToOneField field from UserProfileResource

    class Meta:
        queryset = User.objects.all()
        authorization = DjangoAuthorization()
        #authentication = OAuth20Authentication()
        excludes = ['password', 'is_active', 'is_staff', 'is_superuser', 
            'resource_uri', 'id']
        # disable any http method
        allowed_methods = []
        include_resource_uri = False


class UserProfileResource(MainResource, ModelResource):
    user = fields.ToOneField('ciheul.jendela24.api.UserResource', 'user', full=True)

    class Meta:
        queryset = UserProfile.objects.all()
        authorization = DjangoAuthorization()
        #authentication = OAuth20Authentication()
        resource_name = 'users'
        include_resource_uri = False

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
            return Http404()
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
            return Http404()
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
        # disable any http method
        allowed_methods = []
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
