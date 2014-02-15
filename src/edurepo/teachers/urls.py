from django.conf.urls import patterns, include, url
from teachers import views
from teachers.api import TeacherResource, EntryResource

entry_resource = EntryResource()

urlpatterns = patterns('',
                       url(r'^$', views.index, name='teachers/index'),
                       (r'^api/', include(entry_resource.urls)),
                       url(r'^(?P<teacher_id>[^/]+)/$', views.detail, name='detail'),
                       url(r'^(?P<teacher_id>[^/]+)/(?P<course_id>[^/]+)/$', views.events, name='events'),
                       )
