from tastypie import fields
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from resources.models import Resource
from core.utils import CORSResource


class ResourceResource(CORSResource, ModelResource):

    class Meta:
        queryset = Resource.objects.all()
        resource_name = 'resource'
        filtering = {
            'objective': ALL,
        }
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']

