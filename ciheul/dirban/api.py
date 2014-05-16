from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from ciheul.common import MainResource
from dirban import models


class BusinessResource(MainResource, ModelResource):
    """Resource: /dirban/1.0/business/"""

    class Meta:
        queryset = models.Business.objects.all()
        resource_name = 'business'
        include_resource_uri = False
        excludes = ['id']
        authorization = Authorization()

    def hydrate(self, bundle):
        """Deserializing. POST method."""

        # extract coordinates to longitude and latitude
        lon, lat = bundle.data['coordinates']
        bundle.data['longitude'] = float(lon)
        bundle.data['latitude'] = float(lat)

        # TODO change PIL to Pillow
        #b64save_images(bundle.data['images'])

        return bundle
