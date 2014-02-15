from django.conf.urls import patterns, url
from resources import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='resources/index'),
                       url(r'^(?P<resource_id>[^/]+)/$', views.detail, name='detail'),
                       )
