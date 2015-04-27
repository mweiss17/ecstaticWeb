from __future__ import unicode_literals
from django.contrib import admin
from sds.models import *
from myauth.models import *

class PhotosAdmin(admin.ModelAdmin):
	list_display = ('user', 'photoFile')

class ProfilePictureAdmin(admin.ModelAdmin):
	list_display = ('user', 'photoFile')

class EventsAdmin(admin.ModelAdmin):
	list_display = ('title', 'arrive_start_time','music_start_time', 'event_pic', 'google_map_link', 'location', 'fbEvent', 'eventCity', 'active')
	def event_pic(self, obj):
		return obj.eventPic.photoFile
	def eventCity(self, obj):
		return obj.eventCity.cityName

class UserProfileAdmin(admin.ModelAdmin):
	list_display = ('user', 'profilePic', 'signupDate', 'newsletter')

#I'm not letting users upload music from the backend while it will have the incorrect MIME type
class MusicAdmin(admin.ModelAdmin):
	list_display = ('uploadedSong', 'event', 'song_name_or_link', 'email', 'intention')

class surveySignupsAdmin(admin.ModelAdmin):
	list_display = ('email', 'event', 'mixAccess', 'surveySignupDate')

class globalEventAdmin(admin.ModelAdmin):
	list_display = ('title', 'global_event_pic',)
	def global_event_pic(self, obj):
		return obj.eventPic.photoFile

class cityAdmin(admin.ModelAdmin):
	list_display = ('cityName', 'cityImage',)

admin.site.register(city, cityAdmin)
admin.site.register(globalEvent, globalEventAdmin)
admin.site.register(Music, MusicAdmin)
admin.site.register(Photos, PhotosAdmin)
admin.site.register(Events, EventsAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(surveySignups, surveySignupsAdmin)
