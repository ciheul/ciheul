from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from tastypie import fields
from ciheul.common import MainResource, generate_system_name
from bigpath.models import Shelter, Image
from django.contrib.auth.models import User
from django.contrib.gis.geos import GEOSGeometry

import datetime, base64, os.path

class UserResource(ModelResource):
    #shelter = fields.ToManyField('ShelterResource', 'shelter')
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        fields = ['username', 'last_login']
        allowed_methods = ['get']

class ShelterResource(MainResource, ModelResource):
    user = fields.ForeignKey(UserResource, 'user')
    profile_image = fields.ForeignKey('bigpath.api.ImageResource', 'profile_image', null=True, blank=True)

    class Meta:
        queryset = Shelter.objects.all()
        list_allow_methods = [ 'get', 'post']
        resource_name = 'shelter'
        include_resource_uri = False
        excludes = ['id', 'is_deleted']
        authorization = Authorization()

    def dehydrate(self, bundle):
        """Serializing. GET method."""
        lonlat = GEOSGeometry(bundle.data['coordinates'], srid=32140)
        bundle.data['coordinates'] = list(lonlat.get_coords())

        # get profile pict
        if bundle.obj.profile_image_id is not None:
            profile_pict = Image.objects.get(pk=bundle.obj.profile_image_id)

        if profile_pict is not None:
            bundle.data['profile_image'] = profile_pict.thumbnail.url

        # get images
        images = Image.objects.filter(shelter_id__exact=bundle.obj.id)
        if images is None:
            return bundle

        image_urls = []
        thumbnail_urls = []

        for image in images:
            image_urls.append(image.image.url)
            thumbnail_urls.append(image.thumbnail.url)
        bundle.data['images'] = image_urls
        bundle.data['thumbnails'] = thumbnail_urls

        return bundle

    def hydrate(self, bundle):
        """Deserializing. POST method."""
        bundle.data['created_at'] = datetime.datetime.now()
        bundle.data['updated_at'] = datetime.datetime.now()
        return bundle

class ImageResource(MainResource, ModelResource):
    shelter = fields.ForeignKey(ShelterResource, 'shelter')
    user = fields.ForeignKey(UserResource, 'user')

    class Meta:
        queryset = Image.objects.all()
        list_allow_methods = [ 'get', 'post']
        resource_name = 'image'
        include_resource_uri = True
        excludes = ['id', 'image', 'thumbnail']
        authorization = Authorization()

    def hydrate(self, bundle):
        file_name, ext = os.path.splitext(bundle.data['name'])
        bundle.obj.system_name = generate_system_name() + ext
        bundle.obj.image_file = base64.b64decode(bundle.data['image'])
        bundle.obj.content_type = "image/" + ext[1:]
        return bundle
