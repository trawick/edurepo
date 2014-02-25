__author__ = 'trawick'

from tastypie import fields
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from repo.models import Course, ICan, LearningObjective, GlossaryItem, TrueFalseItem

#### from https://gist.github.com/robhudson/3848832

from django.http import HttpResponse
from tastypie import http
from tastypie.exceptions import ImmediateHttpResponse


class CORSResource(object):
    """
    Adds CORS headers to resources that subclass this.
    """
    def create_response(self, *args, **kwargs):
        response = super(CORSResource, self).create_response(*args, **kwargs)
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Headers'] = 'Content-Type'
        return response

    def method_check(self, request, allowed=None):
        if allowed is None:
            allowed = []

        request_method = request.method.lower()
        allows = ','.join(map(str.upper, allowed))

        if request_method == 'options':
            response = HttpResponse(allows)
            response['Access-Control-Allow-Origin'] = '*'
            response['Access-Control-Allow-Headers'] = 'Content-Type'
            response['Allow'] = allows
            raise ImmediateHttpResponse(response=response)

        if not request_method in allowed:
            response = http.HttpMethodNotAllowed(allows)
            response['Allow'] = allows
            raise ImmediateHttpResponse(response=response)

        return request_method
#### end gist


class CourseResource(CORSResource, ModelResource):
    class Meta:
        queryset = Course.objects.all()
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']


class LearningObjectiveResource(CORSResource, ModelResource):
    course = fields.ForeignKey(CourseResource, 'course', full=False)

    class Meta:
        queryset = LearningObjective.objects.all()
        filtering = {
            'id': ALL,
            'course': ALL_WITH_RELATIONS,
        }
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']


class ICanResource(CORSResource, ModelResource):
    learning_objective = fields.ForeignKey(LearningObjectiveResource, 'learning_objective', full=False)

    class Meta:
        queryset = ICan.objects.all()
        resource_name = "ican"
        filtering = {
            'learning_objective': ALL_WITH_RELATIONS,
            'statement': ALL,
        }
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']


class GlossaryItemResource(CORSResource, ModelResource):
    learning_objective = fields.ForeignKey(LearningObjectiveResource, 'learning_objective', full=False)

    class Meta:
        queryset = GlossaryItem.objects.all()
        resource_name = 'glossary_item'
        filtering = {
            'learning_objective': ALL_WITH_RELATIONS,
            'term': ALL,
            'definition': ALL,
        }
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']


class TrueFalseItemResource(CORSResource, ModelResource):
    learning_objective = fields.ForeignKey(LearningObjectiveResource, 'learning_objective', full=False)

    class Meta:
        queryset = TrueFalseItem.objects.all()
        resource_name = 'true_false_item'
        filtering = {
            'learning_objective': ALL_WITH_RELATIONS,
            'statement': ALL,
            'answer': ALL,
        }
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
