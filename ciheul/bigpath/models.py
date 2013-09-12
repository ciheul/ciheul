from django.db import models
from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile


class Shelter(models.Model):
    name = models.CharField(max_length=50)
    coordinates = models.PointField(srid=32140)
    capacity = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now=True, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    user = models.ForeignKey(User)
    profile_image = models.ForeignKey('bigpath.Image', blank=True, null=True, on_delete=models.SET_NULL, related_name='shelter_profile_image')

    def __unicode__(self):
        return u'%s => %s' % (self.name, self.id)

class Image(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="bigpath/", null=True, blank=True)
    thumbnail = models.ImageField(upload_to="bigpath/thumbnails", null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    shelter = models.ForeignKey(Shelter)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return u'%s => %s' % (self.name, self.id)

    def save(self, *args, **kwargs):
        #self.image = SimpleUploadedFile(self.system_name, self.image_file, getattr(self.image, "content-type", "application/octet-stream"))
        if self.content_type is None:
            self.content_type = "image/jpg"
        self.image = SimpleUploadedFile(self.system_name, self.image_file, self.content_type)
        self.thumbnail = self.create_thumbnail()
        super(Image, self).save(*args, **kwargs)

    def create_thumbnail(self):
        if not self.image:
            return

        import PIL, os
        from cStringIO import StringIO

        THUMBNAIL_SIZE = (200,200)
        DEFAULT_TYPE = 'JPEG'
        image = PIL.Image.open(StringIO(self.image.read()))
        image.thumbnail(THUMBNAIL_SIZE, PIL.Image.ANTIALIAS)

        thumbnail_type = self.content_type.split('/')[1]
        thumbnail_type = thumbnail_type.encode('ascii', 'ignore')

        #set default type
        if thumbnail_type is None:
            thumbnail_type = DEFAULT_TYPE
        elif thumbnail_type == 'jpg' or thumbnail_type == 'JPG':
            thumbnail_type = DEFAULT_TYPE

        temp_handle = StringIO()
        image.save(temp_handle, format=thumbnail_type)
        temp_handle.seek(0)

        return SimpleUploadedFile(self.system_name, temp_handle.read(), content_type=self.content_type)

