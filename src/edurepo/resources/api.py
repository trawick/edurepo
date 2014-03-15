from tastypie import fields
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from resources.models import Resource, ResourceSubmission, ResourceVerification
from core.utils import CORSResource
from repo.api import LearningObjectiveResource


class ResourceResource(CORSResource, ModelResource):

    objective = fields.ForeignKey(LearningObjectiveResource, 'objective', full=False)

    def dehydrate(self, bundle):
        url = bundle.data['url']
        verification = ResourceVerification.objects.filter(url=url)

        extra_data = {'content_type': '',
                      'title': '',
                      'status': ''}
        if len(verification):
            # should be zero or one, but that's not our concern here
            verification = verification[0]
            extra_data['content_type'] = verification.content_type
            extra_data['title'] = verification.document_title
            extra_data['status'] = verification.status_char()

        bundle.data = dict(bundle.data.items() + extra_data.items())
        return bundle

    class Meta:
        queryset = Resource.objects.all()
        resource_name = 'resource'
        filtering = {
            'objective': ALL_WITH_RELATIONS,
        }
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']


class ResourceSubmissionResource(CORSResource, ModelResource):

    resource = fields.ForeignKey(ResourceResource, 'resource', full=False)

    def dehydrate(self, bundle):
        bundle.data['resource_id'] = bundle.obj.resource.id
        return bundle

    class Meta:
        queryset = ResourceSubmission.objects.all().exclude(type='c')
        resource_name = 'resourcesubmission'
        filtering = {
            'resource': ALL_WITH_RELATIONS,
        }
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
