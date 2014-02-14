from django.conf.urls import patterns, include, url
from teachers import views
# from repo.api import CourseResource

# course_resource = CourseResource()

urlpatterns = patterns('',
                       url(r'^$', views.index, name='teachers/index'),
#                       (r'^api/', include(course_resource.urls)),
                       url(r'^(?P<teacher_id>[^/]+)/$', views.detail, name='detail'),
                       url(r'^(?P<teacher_id>[^/]+)/(?P<course_id>[^/]+)/$', views.events, name='events'),
                       )
