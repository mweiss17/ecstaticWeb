from __future__ import unicode_literals
from django import forms
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from sds.perm import perm
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from django.utils import timezone
from datetime import datetime, date, time
import sys


class Photos(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
    photoFile = models.FileField(upload_to='Photos/%Y/%m/%d')
    photographer = models.CharField(max_length=30, blank=True)
    title = models.CharField(max_length=100, blank=True)
    photoUploadDate = models.DateTimeField("photoUploadDate", auto_now=True, blank=True, null=True)
    def __unicode__(self):
        if self.photoFile:
            return unicode(self.photoFile.url)
        else:
            return unicode("/static/img/default_profile_pic.jpg")

class Music(models.Model):
    uploadedSong = models.FileField(upload_to='uploadedSongs/%Y/%m/%d', default='uploadedSongs', blank=True)
    email = models.CharField(max_length=255)
    song_name_or_link = models.CharField(max_length=255, blank=True) #delete after transfer
    intention = models.CharField(max_length=255, blank=True)
    musicUploadDate = models.DateTimeField("musicUploadDate", auto_now=True, blank=True, null=True)
    event = models.ForeignKey("Events", blank=True, null=True)

    def __unicode__(self):
        return self.song_name_or_link+ " : " + self.email + " : " + str(self.musicUploadDate)

class globalEvent(models.Model):
    homepageTagline = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    eventPic = models.ForeignKey(Photos, related_name="globalEventEventPic")
    eventMix = models.ForeignKey(Music, blank=True, null=True, related_name="globalEventEventMix")
    indexHeaderPic = models.ForeignKey(Photos)
    arrive_start_time = models.DateTimeField("Event Start Time")
    music_start_time = models.DateTimeField("Music Start Time")
    def __unicode__(self):
        return self.title


class Events(models.Model):
    active = models.BooleanField()
    title = models.CharField(max_length=100)
    arrive_start_time = models.DateTimeField("Event Start Time")
    music_start_time = models.DateTimeField("Music Start Time")
    eventCity = models.ForeignKey("city", blank=True, null=True)
    location = models.CharField(max_length=50)
    google_map_link = models.CharField(max_length=1000)
    latitude = models.FloatField(default=40.74481)
    longitude = models.FloatField(default=-119.22230)
    eventPic = models.ForeignKey(Photos, related_name="eventsEventPic")
    eventMix = models.ForeignKey(Music, blank=True, null=True)
    fbEvent = models.URLField()
    globalEvent = models.ForeignKey(globalEvent, blank=True, null=True)
    organizer = models.ForeignKey(settings.AUTH_USER_MODEL)

    def __unicode__(self):
        return self.title

class surveySignups(models.Model):
    email = models.CharField(max_length=255)
    event = models.ForeignKey(Events)
    surveySignupDate = models.DateTimeField("signupDate", auto_now=True, default=timezone.now())
    mixAccess = models.CharField(max_length=50, default=":/")

    def __unicode__(self):
        return self.email

class city(models.Model):
    cityName = models.CharField(max_length=255, blank=True)
    cityImage = models.FileField(upload_to='Photos/%Y/%m/%d')
    def __unicode__(self):
        return self.cityName
