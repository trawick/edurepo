from django.conf.urls import patterns, include, url
from teachers import views
from teachers.api import TeacherClassResource, TeacherResource, EntryResource

teacher_resource = TeacherResource()
entry_resource = EntryResource()
teacher_class_resource = TeacherClassResource()

urlpatterns = patterns('',
                       url(r'^$', views.index, name='teachers/index'),
                       (r'^api/', include(entry_resource.urls)),
                       (r'^api/', include(teacher_class_resource.urls)),
                       (r'^api/', include(teacher_resource.urls)),
                       url(r'^(?P<teacher_email>[^/]+)/$', views.detail, name='detail'),
                       url(r'^(?P<teacher_email>[^/]+)/(?P<class_name>[^/]+)/$', views.events, name='events'),
                       )
