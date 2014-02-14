from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from sds import views
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^test.html/$', views.test, name='test'),
    url(r'^form.html/$', views.form, name='form'),
    url(r'^userauth.html/$', views.userauth, name='userauth'),
    url(r'^admin/', include(admin.site.urls)),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

