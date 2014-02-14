from django.conf.urls import patterns, include, url
from repo import views
from repo.api import CourseResource

course_resource = CourseResource()

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^(?P<course_id>[^/]+)/$', views.detail, name='detail'),
                       url(r'^(?P<course_id>[^/]+)/(?P<objective_id>[^/]+)/$', views.by_objective, name='objective'),
                       (r'^api/', include(course_resource.urls)),
                       )
