from django.conf.urls import patterns, include, url
from teachers import views
from teachers.api import TeacherClassResource, TeacherResource, EntryResource

teacher_resource = TeacherResource()
entry_resource = EntryResource()
teacher_class_resource = TeacherClassResource()

urlpatterns = patterns('',
                       url(r'^$', views.index, name='teachers.index'),
                       (r'^api/', include(entry_resource.urls)),
                       (r'^api/', include(teacher_class_resource.urls)),
                       (r'^api/', include(teacher_resource.urls)),
                       url(r'^register/$', 'teachers.views.register_teacher'),
                       url(r'^(?P<teacher_email>[^/]+)/$', views.detail, name='detail'),
                       url(r'^(?P<teacher_email>[^/]+)/add$', 'teachers.views.add_class'),
                       url(r'^(?P<teacher_email>[^/]+)/dashboard$', views.dashboard, name='teachers.views.dashboard'),
                       url(r'^(?P<teacher_email>[^/]+)/(?P<teacher_class_id>[^/]+)/dashboard$', views.dashboard,
                           name='teachers.views.dashboard'),
                       url(r'^(?P<teacher_email>[^/]+)/(?P<teacher_class_id>[^/]+)/(?P<start_of_week>[^/]+)/dashboard$',
                           views.dashboard, name='teachers.views.dashboard'),
                       url(r'^(?P<teacher_email>[^/]+)/(?P<teacher_class_id>[^/]+)/edit_class$',
                           views.edit_class, name='teacher.views.edit_class'),
                       url(r'^(?P<teacher_email>[^/]+)/(?P<teacher_class_id>[^/]+)/(?P<date>[^/]+)/add_objective$',
                           views.add_objective),
                       url(r'^(?P<teacher_email>[^/]+)/(?P<teacher_class_id>[^/]+)/(?P<date>[^/]+)/(?P<objective>[^/]+)/remove_objective$',
                           views.remove_objective),
                       url(r'^(?P<teacher_email>[^/]+)/(?P<class_name>[^/]+)/$', views.events, name='events'),
                       )
