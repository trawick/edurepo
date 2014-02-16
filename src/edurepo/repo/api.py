__author__ = 'trawick'

from tastypie.resources import ModelResource
from repo.models import Course, LearningObjective


class CourseResource(ModelResource):
    class Meta:
        queryset = Course.objects.all()


class LearningObjectiveResource(ModelResource):
    class Meta:
        queryset = LearningObjective.objects.all()
