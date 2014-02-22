from django.conf.urls import include, patterns, url
from resources import views
from resources.api import ResourceResource

resource_resource = ResourceResource()

urlpatterns = patterns('',
                       (r'^api/', include(resource_resource.urls)),
                       url(r'^$', views.index, name='resources/index'),
                       url(r'^(?P<resource_id>[^/]+)/$', views.detail, name='detail'),
                       )
