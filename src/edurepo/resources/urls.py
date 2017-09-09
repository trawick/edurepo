from django.conf.urls import include, patterns, url
from resources import views
from resources.api import ResourceResource, ResourceSubmissionResource

resource_resource = ResourceResource()
resource_submission_resource = ResourceSubmissionResource()

urlpatterns = [
    url(r'^api/', include(resource_resource.urls)),
    url(r'^api/', include(resource_submission_resource.urls)),
    url(r'^$', views.index, name='resources.index'),
    url(r'^create/$', views.create_resource, name='resources.views.create_resource'),
    url(r'^(?P<resource_id>[^/]+)/comment/$', views.comment_on_resource,
        name='resources.views.comment_on_resource'),
    url(r'^(?P<resource_id>[^/]+)/$', views.detail, name='detail'),
]
