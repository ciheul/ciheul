from django.conf.urls import patterns, url, include
from django.contrib import admin
admin.autodiscover()
from tastypie.api import Api

import home.views

from bigear.api import ReportResource
#import bigear.views

from dirban.api import BusinessResource
#import dirban.views

from bigpath.api import ShelterResource, UserResource, ImageResource
import bigpath.views

from juara.api import AdministrativeResource
import juara.views

import bigcrawler.views
import jendela24.views

v1_api = Api(api_name='1.0')
v1_api.register(ReportResource())
v1_api.register(BusinessResource())
v1_api.register(ShelterResource())
v1_api.register(UserResource())
v1_api.register(ImageResource())

v1_juara_api = Api(api_name='1.0')
v1_juara_api.register(AdministrativeResource())

urlpatterns = patterns(
    '',
    url(r'', include('social_auth.urls')),
    url(r'^socket\.io/', jendela24.views.socketio),
    url(r'^jendela24/$', jendela24.views.home),
    url(r'^bigcrawler/$', bigcrawler.views.home),
    url('', home.views.home),
    #(r'^admin/', include(admin.site.urls)),
    #url(r'^juara/', include(v1_juara_api.urls)),
    #url(r'^juara/$', juara.views.home),
    #url(r'^dirban/members/$', dirban.views.members),
    #url(r'^bigear/', include(v1_api.urls)),
    #url(r'^bigear/$', bigear.views.home),
    #url(r'^dirban/', include(v1_api.urls)),
    #url(r'^dirban/$', dirban.views.home),
    #url(r'^bigpath/', include(v1_api.urls)),
    #url(r'^bigpath/$', bigpath.views.home),
)
