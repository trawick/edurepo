from django.conf.urls import patterns, include, url
from repo import views
from repo.api import CourseResource, GlossaryItemResource, LearningObjectiveResource, TrueFalseItemResource

course_resource = CourseResource()
objective_resource = LearningObjectiveResource()
glossary_item_resource = GlossaryItemResource()
true_false_item_resource = TrueFalseItemResource()

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       (r'^api/', include(course_resource.urls)),
                       (r'^api/', include(glossary_item_resource.urls)),
                       (r'^api/', include(objective_resource.urls)),
                       (r'^api/', include(true_false_item_resource.urls)),
                       url(r'^(?P<course_id>[^/]+)/$', views.detail, name='detail'),
                       url(r'^(?P<course_id>[^/]+)/(?P<objective_id>[^/]+)/$', views.by_objective, name='objective'),
                       )
