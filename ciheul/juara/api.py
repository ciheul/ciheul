from tastypie.resources import ModelResource
#from tastypie.authorization import Authorization
#from ciheul.common import MainResource
from juara import models


class AdministrativeResource(ModelResource):

    class Meta:
        queryset = models.Administrative.objects.all()
        resource_name = 'administrative'
        include_resource_uri = False
        excludes = ['id']
        limit = 50
        #authorization = Authorization()

    def alter_list_data_to_serialize(self, request, response):
        """GET /juara/1.0/administrative"""

        # rename 'objects' to 'data'
        response['data'] = response['objects']
        del(response['objects'])

        # add code status
        response['meta']['code'] = 200

        return response

    def alter_detail_data_to_serialize(self, request, response):
        """GET /juara/1.0/administrative/<administrative_id>"""

        modified_response = {}
        modified_response['meta'] = {}
        modified_response['meta']['code'] = 200
        modified_response['data'] = response

        return modified_response
