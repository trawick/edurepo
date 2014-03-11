from tastypie import fields
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from resources.models import Resource
from core.utils import CORSResource
from repo.api import LearningObjectiveResource


class ResourceResource(CORSResource, ModelResource):

    objective = fields.ForeignKey(LearningObjectiveResource, 'objective', full=False)

    class Meta:
        queryset = Resource.objects.all()
        resource_name = 'resource'
        filtering = {
            'objective': ALL_WITH_RELATIONS,
        }
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']

