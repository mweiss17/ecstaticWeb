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
    url(r'^accounts/auth/$',  'sds.views.auth_view'),    
    url(r'^accounts/', include('allauth.urls')), 
    url(r'^add_email_to_mailing_list/$', views.add_email_to_mailing_list),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^appindex.html/$', views.appindex, name='contact'),
    url(r'^citypage_getthemix.html/$', views.citypage_getthemix, name='citypage_getthemix'),
    url(r'^citypage_city.html/$', views.citypage_city, name='citypage_city'),
    url(r'^comments/', include('django.contrib.comments.urls')),
    url(r'^confirm/(?P<activation_key>\w+)/', views.register_confirm),
    url(r'^contact.html/$', views.contact, name='contact'),
    url(r'^createprofile.html/$', views.createprofile, name='createprofile'),
    url(r'^event_creation_success.html/', views.event_creation_success, name='event_creation_success'),
    url(r'^future.html/$', views.future, name='future'),
    url(r'^jointhesquad.html/$', views.jointhesquad, name='jointhesquad'),
    url(r'^logout.html/$', views.logout, name='logout'),
    url(r'^mailchimp/', include('mailchimp.urls')),
    url(r'^mission.html/$', views.mission, name='mission'),
    url(r'^mixMailSignup/$', views.mixMailSignup),
    url(r'^NuitBlanche/$', views.index),
    url(r'^organize.html/$', views.organize, name='organize'),
    url(r'^participate.html/$', views.participate, name='participate'),
    url(r'^profile.html/$', views.profile, name='profile'),
    url(r'^profileupdate/$', views.profileupdate, name='profileupdate'),    
    url(r'^register_success.html/$', views.register_success, name='register_success'),
    url(r'^stream.html/$', views.stream, name='stream'),
    url(r'^userauth.html/$', views.userauth, name='userauth'),
    url(r'^weblog/', include('zinnia.urls')),
    url(r'^whatissds.html/$', views.whatissds, name='whatissds'),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
