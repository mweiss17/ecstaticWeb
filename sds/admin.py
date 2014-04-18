from django.contrib import admin
from sds.models import Photos, Music, Events, UserProfile, potentialOrganizer

class PhotosAdmin(admin.ModelAdmin):
	list_display = ('photographer', 'pictureType', 'photoFile')

class MusicAdmin(admin.ModelAdmin):
	list_display = ('song_name_or_link', 'songname', 'email', 'intention')

class EventsAdmin(admin.ModelAdmin):
	list_display = ('title', 'start_time', 'event_pic', 'google_map_link', 'location', 'fbEvent')
	def event_pic(self, obj):
		return obj.eventPic.photoFile

class UserProfileAdmin(admin.ModelAdmin):
	list_display = ('user', 'profilePic', 'signupDate')

class potentialOrganizerAdmin(admin.ModelAdmin):
	list_display = ('name', 'email', 'city', 'why')

admin.site.register(Photos, PhotosAdmin)
admin.site.register(Music, MusicAdmin)
admin.site.register(Events, EventsAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(potentialOrganizer, potentialOrganizerAdmin)