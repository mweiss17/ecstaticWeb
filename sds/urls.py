from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from sds import views
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^about.html/$', views.about, name='about'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^appindex/$', views.appindex, name='contact'),
    url(r'^citypage_city.html/$', views.citypage_city, name='citypage_city'),
    url(r'^comments/', include('django.contrib.comments.urls')),
    url(r'^contact.html/$', views.contact, name='contact'),
    url(r'^event_creation_success.html/', views.event_creation_success, name='event_creation_success'),
    url(r'^future.html/$', views.future, name='future'),
    url(r'^logout.html/$', views.logout, name='logout'),
    url(r'^mailchimp/', include('mailchimp.urls')),
    url(r'^organize.html/$', views.organize, name='organize'),
    url(r'^register_success.html/$', views.register_success, name='register_success'),
    url(r'^stream.html/$', views.stream, name='stream'),
    url(r'^weblog/', include('zinnia.urls')),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
