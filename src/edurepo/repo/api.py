__author__ = 'trawick'

from tastypie.resources import ModelResource
from repo.models import Course


class CourseResource(ModelResource):
    class Meta:
        queryset = Course.objects.all()

