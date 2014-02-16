from tastypie import fields
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from teachers.models import Teacher, Course, Entry


class TeacherResource(ModelResource):

    class Meta:
        queryset = Teacher.objects.all()
        resource_name = 'teacher'
        filtering = {
            'email': ALL,
            'name': ALL,
        }


class CourseResource(ModelResource):

    class Meta:
        queryset = Course.objects.all()
        resource_name = 'course'
        filtering = {
            'name': ALL,
        }


class EntryResource(ModelResource):

    teacher = fields.ForeignKey(TeacherResource, 'teacher')
    course = fields.ForeignKey(CourseResource, 'course')

    class Meta:
        queryset = Entry.objects.all()
        resource_name = 'entry'
        filtering = {
            'teacher': ALL_WITH_RELATIONS,
            'course': ALL_WITH_RELATIONS,
            'date': ALL,
            'teacher_name': ALL_WITH_RELATIONS
        }
