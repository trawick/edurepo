from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # url(r'^$', 'edurepo.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^repo/', include('repo.urls')),
    url(r'^teachers/', include('teachers.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
