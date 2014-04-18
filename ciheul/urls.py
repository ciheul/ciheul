from django.contrib.auth.views import login, logout
from django.conf.urls import patterns, url, include
from django.contrib import admin
admin.autodiscover()

from tastypie.api import Api

from bigear.api import ReportResource
from bigpath.api import ShelterResource, UserResource, ImageResource
from dirban.api import BusinessResource
from juara.api import AdministrativeResource
from jendela24.api import RssNewsResource, UserResource, ActivitiesResource, UserProfileResource


v1_api = Api(api_name='1.0')
v1_api.register(ReportResource())
v1_api.register(BusinessResource())
v1_api.register(ShelterResource())
v1_api.register(UserResource())
v1_api.register(ImageResource())

v1_jendela24_api = Api(api_name='1.0')
v1_jendela24_api.register(RssNewsResource())
v1_jendela24_api.register(UserResource())
v1_jendela24_api.register(UserProfileResource())
v1_jendela24_api.register(ActivitiesResource())

v1_juara_api = Api(api_name='1.0')
v1_juara_api.register(AdministrativeResource())

urlpatterns = patterns('',
    (r'^admin/?', include(admin.site.urls)),
    url(r'^socket\.io/', 'jendela24.views.socketio'),
    url(r'^jendela24/', include(v1_jendela24_api.urls)),
    url(r'^jendela24/$', 'jendela24.views.home'),

    url(r'^login/redirect', 'accounts.views.redirect_twitter'),
    #url(r'^login/redirect', 'accounts.views.profile'),

    url(r'^accounts/register', 'accounts.views.register'),
    url(r'^accounts/logout', 'accounts.views.logout'),
    url(r'^accounts/login_twitter', 'accounts.views.login_twitter'),
    url(r'^accounts/login', 'accounts.views.login_form'),
    url(r'^accounts/redirect', 'accounts.views.redirect'),
    url(r'^accounts/profile', 'accounts.views.profile'),
    url(r'^accounts/settings', 'accounts.views.settings'),
    url(r'^accounts', 'accounts.views.login_form'),
    url(r'', include('social.apps.django_app.urls', namespace='social')),

    #url(r'^bigcrawler/$', bigcrawler.views.home),
    #url(r'^juara/', include(v1_juara_api.urls)),
    #url(r'^juara/$', juara.views.home),
    #url(r'^dirban/members/$', dirban.views.members),
    #url(r'^bigear/', include(v1_api.urls)),
    #url(r'^bigear/$', bigear.views.home),
    #url(r'^dirban/', include(v1_api.urls)),
    #url(r'^dirban/$', dirban.views.home),
    #url(r'^bigpath/', include(v1_api.urls)),
    #url(r'^bigpath/$', bigpath.views.home),
    url(r'^oauth2/', include('provider.oauth2.urls', namespace='oauth2')),
    url('', 'home.views.home'),
)
