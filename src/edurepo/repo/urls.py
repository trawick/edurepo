from django.conf.urls import patterns, include, url
from repo import views
from repo.api import CourseResource

course_resource = CourseResource()

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       (r'^api/', include(course_resource.urls)),
                       )
