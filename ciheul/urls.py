from django.conf.urls import patterns, url, include
from django.contrib import admin
admin.autodiscover()
from tastypie.api import Api

import home.views

from bigear.api import ReportResource
import bigear.views

from dirban.api import BusinessResource
import dirban.views

from bigpath.api import ShelterResource, UserResource, ImageResource
import bigpath.views


v1_api = Api(api_name='1.0')
v1_api.register(ReportResource())
v1_api.register(BusinessResource())
v1_api.register(ShelterResource())
v1_api.register(UserResource())
v1_api.register(ImageResource())

urlpatterns = patterns(
    '',
    (r'^admin/', include(admin.site.urls)),
    url(r'', include('social_auth.urls')),
    #url(r'^dirban/members/$', dirban.views.members),
    #url(r'^bigear/', include(v1_api.urls)),
    #url(r'^bigear/$', bigear.views.home),
    #url(r'^dirban/', include(v1_api.urls)),
    #url(r'^dirban/$', dirban.views.home),
    url(r'^bigpath/', include(v1_api.urls)),
    url(r'^bigpath/$', bigpath.views.home),
    #url(r'', home.views.home),
)
