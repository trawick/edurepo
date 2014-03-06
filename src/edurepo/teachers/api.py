from tastypie import fields
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from teachers.models import Teacher, TeacherClass, Entry
from core.utils import CORSResource


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
