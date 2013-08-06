from django.conf.urls import patterns, url, include
from tastypie.api import Api
from bigear.api import ReportResource
from dirban.api import BusinessResource
from bigear.views import home


v1_api = Api(api_name='1.0')
v1_api.register(ReportResource())
v1_api.register(BusinessResource())

urlpatterns = patterns(
    '',
    url(r'^bigear/', include(v1_api.urls)),
    url(r'^bigear/$', home),
    url(r'^dirban/', include(v1_api.urls)),
)
