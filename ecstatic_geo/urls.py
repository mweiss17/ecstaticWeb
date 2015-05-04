from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin
from ecstatic_geo import views
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'^post_location/$', views.post_location, name='post_location'),
    url(r'^get_most_recent_location/$', views.get_most_recent_location, name='get_most_recent_location'),
    url(r'^get_nearest_users/$', views.get_nearest_users, name='get_nearest_users'),
)