from django.contrib import admin
from sds.models import Photos, Events

class PhotosAdmin(admin.ModelAdmin):
	list_display = ('url', 'user_id')

admin.site.register(Photos, PhotosAdmin)
