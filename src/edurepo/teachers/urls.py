from django.conf.urls import include, url
from teachers import views
from teachers.api import TeacherClassResource, TeacherResource, EntryResource

teacher_resource = TeacherResource()
entry_resource = EntryResource()
teacher_class_resource = TeacherClassResource()

urlpatterns = [
    url(r'^$', views.index, name='teachers.index'),
    url(r'^api/', include(entry_resource.urls)),
    url(r'^api/', include(teacher_class_resource.urls)),
    url(r'^api/', include(teacher_resource.urls)),
    url(r'^register/$', views.register_teacher, name='register-teacher'),
    url(r'^(?P<teacher_email>[^/]+)/$', views.detail, name='detail'),
    url(r'^(?P<teacher_email>[^/]+)/add$', views.add_class, name='add-class'),
    url(r'^(?P<teacher_email>[^/]+)/dashboard$', views.dashboard, name='teachers.views.dashboard'),
    url(r'^(?P<teacher_email>[^/]+)/(?P<teacher_class_id>[^/]+)/dashboard$', views.dashboard,
        name='teachers.views.dashboard'),
    url(r'^(?P<teacher_email>[^/]+)/(?P<teacher_class_id>[^/]+)/(?P<start_of_week>[^/]+)/dashboard$',
       views.dashboard, name='teachers.views.dashboard'),
    url(r'^(?P<teacher_email>[^/]+)/(?P<teacher_class_id>[^/]+)/edit_class$',
       views.edit_class, name='teacher.views.edit_class'),
    url(r'^(?P<teacher_email>[^/]+)/(?P<teacher_class_id>[^/]+)/(?P<date>[^/]+)/add_objective$',
       views.add_objective, name='add-objective'),
    url(r'^(?P<teacher_email>[^/]+)/(?P<teacher_class_id>[^/]+)/(?P<date>[^/]+)/(?P<objective>[^/]+)/remove_objective$',
       views.remove_objective, name='remove-objective'),
    url(r'^(?P<teacher_email>[^/]+)/(?P<class_name>[^/]+)/$', views.events, name='events'),
]
