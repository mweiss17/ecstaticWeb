from django.db import models
from django.contrib import admin
from django.forms import ModelForm
import datetime

class Photos(models.Model):
    url = models.CharField(max_length=100)
    user_id = models.CharField(max_length=30)
    photographer = models.CharField(max_length=30)
    
    @classmethod
    def create(cls, url, user_id, photographer):
        image = cls(url=url, user_id=user_id, photographer=photographer)
        return image

class Events(models.Model):
    title = models.CharField(max_length=100)
    start_time = models.DateTimeField("Event Time")
    location = models.CharField(max_length=50)
    google_map_link = models.CharField(max_length=200)

class Music(models.Model):
    #uploadedSong = models.FileField(upload_to='uploadedSongs/%Y/$m/$d')
    email = models.CharField(max_length=255)
    songname = models.CharField(max_length=255)
    intention = models.CharField(max_length=255)

class MusicForm(ModelForm):
    class Meta:
        model = Music
        fields = ['email', 'songname', 'intention']