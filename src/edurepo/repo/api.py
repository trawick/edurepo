__author__ = 'trawick'

from tastypie import fields
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from repo.models import Course, CourseCategory, ICan, LearningObjective, GlossaryItem, MultipleChoiceItem, ReferenceText, TrueFalseItem
from core.utils import CORSResource


class CourseCategoryResource(CORSResource, ModelResource):
    class Meta:
        queryset = CourseCategory.objects.all()
        filtering = {
            'id': ALL,
        }
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']


class CourseResource(CORSResource, ModelResource):
    cat = fields.ForeignKey(CourseCategoryResource, 'cat', full=False)

    class Meta:
        queryset = Course.objects.all()
        filtering = {
            'cat': ALL_WITH_RELATIONS,
            'id': ALL,
        }
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']


class LearningObjectiveResource(CORSResource, ModelResource):
    course = fields.ForeignKey(CourseResource, 'course', full=False)

    class Meta:
        limit = 70
        queryset = LearningObjective.objects.all().order_by('id')
        filtering = {
            'id': ALL,
            'course': ALL_WITH_RELATIONS,
        }
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']


class ReferenceTextResource(CORSResource, ModelResource):
    learning_objective = fields.ForeignKey(LearningObjectiveResource, 'learning_objective', full=False)

    class Meta:
        queryset = ReferenceText.objects.all()
        filtering = {
            'learning_objective': ALL_WITH_RELATIONS,
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


class MultipleChoiceItemResource(CORSResource, ModelResource):
    learning_objective = fields.ForeignKey(LearningObjectiveResource, 'learning_objective', full=False)

    class Meta:
        queryset = MultipleChoiceItem.objects.all()
        filtering = {
            'learning_objective': ALL_WITH_RELATIONS,
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
