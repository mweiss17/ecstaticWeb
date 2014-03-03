from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from sds import views
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^form.html/$', views.form, name='form'),
    url(r'^userauth.html/$', views.userauth, name='userauth'),
    url(r'^future.html/$', views.future, name='future'),
    url(r'^become.html/$', views.become, name='become'),
    url(r'^participate.html/$', views.participate, name='participate'),
    url(r'^jointhesquad.html/$', views.jointhesquad, name='jointhesquad'),
    url(r'^whatissds.html/$', views.whatissds, name='whatissds'),
    url(r'^admin/', include(admin.site.urls)),

) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

