from django.db import models
from django.contrib import admin
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
    host = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    google_map_link = models.CharField(max_length=200)