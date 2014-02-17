from tastypie import fields
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from teachers.models import Teacher, TeacherClass, Entry

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


class TeacherResource(CORSResource, ModelResource):

    class Meta:
        queryset = Teacher.objects.all()
        resource_name = 'teacher'
        filtering = {
            'email': ALL,
            'name': ALL,
        }
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']


class TeacherClassResource(CORSResource, ModelResource):

    teacher = fields.ForeignKey(TeacherResource, 'teacher')

    class Meta:
        queryset = TeacherClass.objects.all()
        resource_name = 'teacher_class'
        filtering = {
            'teacher': ALL_WITH_RELATIONS,
            'name': ALL_WITH_RELATIONS,
            'course_id': ALL,
        }
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']


class EntryResource(CORSResource, ModelResource):

    teacher = fields.ForeignKey(TeacherResource, 'teacher', full=True)
    teacher_class = fields.ForeignKey(TeacherClassResource, 'teacher_class', full=True)

    class Meta:
        queryset = Entry.objects.all()
        resource_name = 'entry'
        filtering = {
            'teacher': ALL_WITH_RELATIONS,
            'teacher_class': ALL_WITH_RELATIONS,
            'date': ALL,
            'teacher_name': ALL_WITH_RELATIONS
        }
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
