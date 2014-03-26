from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView
from repo import views as repo_views

admin.autodiscover()

urlpatterns = patterns('',
    # url(r'^$', 'edurepo.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^repo/', include('repo.urls')),
    url(r'^teachers/', include('teachers.urls')),
    url(r'^resources/', include('resources.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^logout/', repo_views.logout, name='logout'),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='top.index')
)
