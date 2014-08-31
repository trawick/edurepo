from django.conf.urls import patterns, include, url
from repo import views
from repo.api import CourseResource, CourseCategoryResource, GlossaryItemResource, ICanResource, \
    LearningObjectiveResource, MultipleChoiceItemResource, ReferenceTextResource, TrueFalseItemResource

course_resource = CourseResource()
course_category_resource = CourseCategoryResource()
ican_resource = ICanResource()
objective_resource = LearningObjectiveResource()
glossary_item_resource = GlossaryItemResource()
multiple_choice_item_resource = MultipleChoiceItemResource()
reference_text_resource = ReferenceTextResource()
true_false_item_resource = TrueFalseItemResource()

urlpatterns = patterns('',
                       url(r'^$', views.index, name='repo.index'),
                       (r'^api/', include(course_resource.urls)),
                       (r'^api/', include(course_category_resource.urls)),
                       (r'^api/', include(glossary_item_resource.urls)),
                       (r'^api/', include(ican_resource.urls)),
                       (r'^api/', include(multiple_choice_item_resource.urls)),
                       (r'^api/', include(objective_resource.urls)),
                       (r'^api/', include(reference_text_resource.urls)),
                       (r'^api/', include(true_false_item_resource.urls)),
                       url(r'^(?P<course_id>[^/]+)/$', views.detail, name='detail'),
                       url(r'^(?P<course_id>[^/]+)/(?P<objective_id>[^/]+)/$', views.by_objective, name='objective'),
                       )
