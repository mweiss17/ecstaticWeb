from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from myauth import views
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'^loginView/$', views.loginView, name='loginView'),
    url(r'^loginViewiOS/$', views.loginViewiOS, name='loginViewiOS'),
    url(r'^forgotpassword.html/$', views.forgotpassword, name='forgotpassword'),
    url(r'^profile.html/$', views.profile, name='profile'),
    url(r'^createprofile.html/$', views.createprofile, name='createprofile'),
    url(r'^createprofileiOS/$', views.createprofileiOS, name='createprofileiOS'),
    url(r'^profileupdate/$', views.profileupdate, name='profileupdate'),    
)