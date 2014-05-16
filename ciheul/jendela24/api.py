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
from boilerpipe.extract import Extractor
from ciheul.common import MainResource, get_current_session
from jendela24.models import Activities, ArticleStat, RssNews, UserProfile

from datetime import date


class RssNewsResource(MainResource, ModelResource):
    """Resource: /jendela24/1.0/news/"""

    class Meta:
        queryset = RssNews.objects.all().order_by('published_at').reverse()
        resource_name = 'news'
        include_resource_uri = False
        #excludes = ['id']
        authorization = Authorization()
        paginator_class = Paginator

    def dehydrate(self, bundle):
        """GET Method"""
        
        #print bundle.data['content']
        if bundle.data['content']:
            extractor = Extractor(extractor='ArticleExtractor', html=bundle.data['content'])
            bundle.data['content'] = extractor.getText()

        try:
            article_stats = ArticleStat.objects.filter(article_id=bundle.obj.id)
            bundle.data['stat'] = {
                'reads': sum(map(lambda x: x.reads, article_stats)),
                'likes': sum(map(lambda x: x.likes, article_stats)),
                'dislikes': sum(map(lambda x: x.dislikes, article_stats)),
                'shares': sum(map(lambda x: x.shares, article_stats)),
            }
        except ObjectDoesNotExist:
            bundle.data['stat'] = {
                'reads': 0, 
                'likes': 0, 
                'dislikes': 0,
                'shares': 0,
            }

        # no cookies or no sessionid field in cookies, then just send normal
        # newsfeed to anonymous user
        if not bundle.request.COOKIES or not bundle.request.COOKIES['sessionid']:
            return bundle

        try:
            # even if there is a cookie, sessionid field might be not exist,
            # then it is also anonymous user
            s = get_current_session(bundle.request.COOKIES['sessionid'])
            if s is None or 'user_id' not in s:
                return bundle

            # get activity information whether user has already
            # read/liked/shared
            activity = Activities.objects.get(user_id=s['user_id'], \
                article_id=bundle.obj.id)

            # assign information 
            bundle.data['activity'] = {
                'read': activity.like or activity.share,
                'like': activity.like,
                'dislike': activity.dislike,
                'share': activity.share
            }
        except ObjectDoesNotExist:
            # assign False if the news has never been opened
            bundle.data['activity'] = {
                'read': False, 
                'like': False, 
                'dislike': False, 
                'share': False
            }

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

            # POST dislike
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/dislike%s$" % \
                (self._meta.resource_name, trailing_slash()), \
                self.wrap_view('post_dislike'), name="api_post_dislike"),

            # POST canceldislike
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/canceldislike%s$" % \
                (self._meta.resource_name, trailing_slash()), \
                self.wrap_view('post_canceldislike'), \
                name="api_post_canceldislike"),

            # POST share 
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/share%s$" % \
                (self._meta.resource_name, trailing_slash()), \
                self.wrap_view('post_share'), name="api_post_share"),
        ]

    def get_likes(self, request, **kwargs):
        """
        GET /news/<article_id>/likes
        """
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
        return activities_resource.get_detail(request, article_id=obj.pk, \
            like=True)

    def post_read(self, request, **kwargs):
        """
        POST /news/<article_id>/read
        """
        try:
            article_stat = ArticleStat.objects.get(article_id=kwargs['pk'], \
                date=date.today())
            article_stat.reads += 1
            article_stat.save()
        except ObjectDoesNotExist:
            ArticleStat.objects.create(article_id=kwargs['pk'], \
                date=date.today(), reads=1, likes=0, shares=0)

        try:
            # check whether user has opened the article
            s = Session.objects.get(pk=request.COOKIES['sessionid']).get_decoded()
            a = Activities.objects.filter(user_id=s['user_id'], \
                article_id=kwargs['pk'])
            if not a:
                # if not, create a new one
                Activities.objects.create(user_id=s['user_id'], \
                    article_id=kwargs['pk'], like=False, share=False)
            else:
                # just ignore, data has been created before
                return HttpAccepted()
        except Exception:
            # just ignore AnonymousUser
            return HttpAccepted() 
        return HttpCreated()

    def post_like(self, request, **kwargs):
        """
        POST /news/<article_id>/like
        """
        try:
            s = Session.objects.get(pk=request.COOKIES['sessionid']).get_decoded()
            print s

            activity = Activities.objects.get(user_id=s['user_id'], \
                article_id=kwargs['pk'])
            print activity

            try:
                article_stat = ArticleStat.objects.get(article_id=kwargs['pk'], \
                    date=date.today())
            except ObjectDoesNotExist:
                pass

            if activity.like == False and activity.dislike == False:
                activity.like = True

                article_stat.likes += 1

                activity.save()
                article_stat.save()
            elif activity.like == True and activity.dislike == False:
                pass
            elif activity.like == False and activity.dislike == True:
                activity.like = True
                activity.dislike = False

                article_stat.likes += 1
                article_stat.dislikes -= 1

                activity.save()
                article_stat.save()
            else:
                print "[ERROR] Like and Dislike cannot be True at the same time."
        except ObjectDoesNotExist:
            Activities.objects.create(user_id=s['user_id'], \
                article_id=kwargs['pk'], like=True, share=False)
        except Exception:
            print "guest"
            # TODO http status does not work properly
            return Http404() 
        return HttpCreated()

    def post_unlike(self, request, **kwargs):
        """
        POST /news/<article_id>/unlike
        """
        try:
            s = Session.objects.get(pk=request.COOKIES['sessionid']).get_decoded()

            activity = Activities.objects.get(user_id=s['user_id'], \
                article_id=kwargs['pk'])

            try:
                article_stat = ArticleStat.objects.get(article_id=kwargs['pk'], \
                    date=date.today())
                article_stat.likes -= 1
                article_stat.save()
            except ObjectDoesNotExist:
                pass

            activity.like = False
            activity.save()
        except ObjectDoesNotExist:
            raise BadRequest('Activitiy does not exist.')
        return HttpCreated()

    def post_dislike(self, request, **kwargs):
        """
        POST /news/<article_id>/dislike
        """
        try:
            s = Session.objects.get(pk=request.COOKIES['sessionid']).get_decoded()

            activity = Activities.objects.get(user_id=s['user_id'], \
                article_id=kwargs['pk'])

            try:
                article_stat = ArticleStat.objects.get(article_id=kwargs['pk'], \
                    date=date.today())
            except ObjectDoesNotExist:
                pass

            if activity.like == False and activity.dislike == False:
                activity.dislike = True

                article_stat.dislikes += 1

                activity.save()
                article_stat.save()
            elif activity.like == True and activity.dislike == False:
                activity.like = False 
                activity.dislike = True

                article_stat.likes -= 1
                article_stat.dislikes += 1

                activity.save()
                article_stat.save()
            elif activity.like == False and activity.dislike == True:
                pass
            else:
                print "[ERROR] Like and Dislike cannot be True at the same time."
        except ObjectDoesNotExist:
            Activities.objects.create(user_id=s['user_id'], \
                article_id=kwargs['pk'], like=True, share=False)
        except Exception:
            print "guest"
            # TODO http status does not work properly
            return Http404() 
        return HttpCreated()

    def post_canceldislike(self, request, **kwargs):
        """
        POST /news/<article_id>/canceldislike
        """
        try:
            s = Session.objects.get(pk=request.COOKIES['sessionid']).get_decoded()

            activity = Activities.objects.get(user_id=s['user_id'], \
                article_id=kwargs['pk'])

            try:
                article_stat = ArticleStat.objects.get(article_id=kwargs['pk'], \
                    date=date.today())
                article_stat.dislikes -= 1
                article_stat.save()
            except ObjectDoesNotExist:
                pass

            activity.dislike = False
            activity.save()
        except ObjectDoesNotExist:
            raise BadRequest('Activitiy does not exist.')
        return HttpCreated()

    def post_share(self, request, **kwargs):
        """
        POST /news/<article_id>/share
        """
        try:
            article_stat = ArticleStat.objects.get(article_id=kwargs['pk'], \
                date=date.today())
            article_stat.shares += 1
            article_stat.save()
        except ObjectDoesNotExist:
            pass

        try:
            s = Session.objects.get(pk=request.COOKIES['sessionid']).get_decoded()

            activity = Activities.objects.get(user_id=s['user_id'], \
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

            # GET dislikes
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/dislikes%s$" % \
                (self._meta.resource_name, trailing_slash()), \
                self.wrap_view('get_dislikes'), name="user_get_dislikes"),

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

    def get_dislikes(self, request, **kwargs):
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
        return activities_resource.get_list(request, user=obj.pk, dislike=True)

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
    user = fields.ToOneField(UserProfileResource, 'user', full=True)
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
            'dislike': ALL,
            'share': ALL,
        }
        ordering = []


# http://django-tastypie.readthedocs.org/en/latest/cookbook.html
# http://stackoverflow.com/questions/14085865/exposing-model-method-with-tastypie
