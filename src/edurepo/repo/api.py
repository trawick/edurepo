__author__ = 'trawick'

from tastypie.resources import ModelResource
from repo.models import Course, LearningObjective

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
    class Meta:
        queryset = LearningObjective.objects.all()
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
