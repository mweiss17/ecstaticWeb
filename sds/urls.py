from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from sds import views
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^contact.html/$', views.contact, name='contact'),
    url(r'^mission.html/$', views.mission, name='mission'),
    url(r'^form.html/$', views.form, name='form'),
    url(r'^userauth.html/$', views.userauth, name='userauth'),
    url(r'^future.html/$', views.future, name='future'),
    url(r'^past.html/$', views.past, name='past'),
    url(r'^become.html/$', views.become, name='become'),
    url(r'^participate.html/$', views.participate, name='participate'),
    url(r'^jointhesquad.html/$', views.jointhesquad, name='jointhesquad'),
    url(r'^whatissds.html/$', views.whatissds, name='whatissds'),
    url(r'^stream.html/$', views.stream, name='stream'),
    url(r'^appindex.html/$', views.appindex, name='contact'),
    url(r'^accounts/login/$',  'sds.views.login'),
    url(r'^accounts/auth/$',  'sds.views.auth_view'),    
    url(r'^accounts/logout/$', 'sds.views.logout'),
    url(r'^accounts/loggedin/$', 'sds.views.loggedin'),
    url(r'^accounts/invalid/$', 'sds.views.invalid_login'),
    url(r'^add_email_to_mailing_list/$', views.add_email_to_mailing_list),
    url(r'^accounts/', include('allauth.urls')), 
    url(r'^mailchimp/', include('mailchimp.urls')),
    url(r'^admin/', include(admin.site.urls))

) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

