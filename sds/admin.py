from django.contrib import admin
from sds.models import Photos, Music, Events, UserProfile

class PhotosAdmin(admin.ModelAdmin):
	list_display = ('photographer', 'pictureType', 'photoFile')

class MusicAdmin(admin.ModelAdmin):
	list_display = ('songname', 'email', 'intention')

class EventsAdmin(admin.ModelAdmin):
	list_display = ('title', 'start_time', 'eventPic', 'google_map_link', 'location', 'fbEvent')

class UserProfileAdmin(admin.ModelAdmin):
	list_display = ('user', 'profilePic', 'signupDate')

admin.site.register(Photos, PhotosAdmin)
admin.site.register(Music, MusicAdmin)
admin.site.register(Events, EventsAdmin)
admin.site.register(UserProfile, UserProfileAdmin)