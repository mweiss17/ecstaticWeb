from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from ecstatic_geo import urls
from myauth import urls
from sds import urls
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import *

urlpatterns = patterns('',
	url(r'^', include('sds.urls')),
	url(r'^geo/', include('ecstatic_geo.urls')),
	url(r'^auth/', include('myauth.urls')),
    (r'^accounts/password/reset/done/$', 'django.contrib.auth.views.password_reset_done'),
    (r'^accounts/password/reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm',
     {'post_reset_redirect' : '/accounts/password/done/'}),
    (r'^accounts/password/done/$', 'django.contrib.auth.views.password_reset_complete', {'template_name': 'myauth/passwordresetdone.html'}),
    url('', include('social.apps.django_app.urls', namespace='social')),
    #url('', include('django.contrib.auth.urls', namespace='auth')),
)