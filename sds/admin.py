from django.contrib import admin
from sds.models import Photos, ProfilePicture, Music, Events, UserProfile, globalEvent

class PhotosAdmin(admin.ModelAdmin):
	list_display = ('user', 'photoFile')

class ProfilePictureAdmin(admin.ModelAdmin):
	list_display = ('user', 'photoFile')

class EventsAdmin(admin.ModelAdmin):
	list_display = ('title', 'arrive_start_time','music_start_time', 'event_pic', 'google_map_link', 'location', 'fbEvent')
	def event_pic(self, obj):
		return obj.eventPic.photoFile

class UserProfileAdmin(admin.ModelAdmin):
	list_display = ('user', 'profilePic', 'signupDate')

#I'm not letting users upload music from the backend while it will have the incorrect MIME type
class MusicAdmin(admin.ModelAdmin):
	list_display = ('uploadedSong', 'event', 'song_name_or_link', 'email', 'intention')

class globalEventAdmin(admin.ModelAdmin):
	list_display = ('title', 'global_event_pic',)
	def global_event_pic(self, obj):
		return obj.eventPic.photoFile

admin.site.register(globalEvent, globalEventAdmin)
admin.site.register(Music, MusicAdmin)
admin.site.register(Photos, PhotosAdmin)
admin.site.register(ProfilePicture, ProfilePictureAdmin)
admin.site.register(Events, EventsAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
