from django.conf.urls import include, url
from django.contrib import admin
from repo import views as repo_views
from edurepo import views as edurepo_views

admin.autodiscover()

urlpatterns = [
     # url(r'^$', 'edurepo.views.home', name='home'),
     # url(r'^blog/', include('blog.urls')),

     url(r'^repo/', include('repo.urls')),
     url(r'^teachers/', include('teachers.urls')),
     url(r'^resources/', include('resources.urls')),
     url(r'^admin/', admin.site.urls),
     url(r'^logout/', repo_views.logout, name='logout'),
     url('', include('social_django.urls', namespace='social')),
     url(r'^$', edurepo_views.welcome, name='top.index'),
]
