from django import forms
from django.db import models
from django.contrib import admin
from django.forms import ModelForm
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
import datetime


class Photos(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True)
    photoFile = models.FileField(upload_to='Photos/%Y/%m/%d')
    photographer = models.CharField(max_length=30, blank=True)
    title = models.CharField(max_length=100)
    photoUploadDate = models.DateTimeField("photoUploadDate", auto_now=True, blank=True, null=True)
    def __unicode__(self):
        return self.title + " : " + self.user.username + " : " + str(self.photoUploadDate)

class ProfilePicture(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    photoFile = models.FileField(upload_to='Photos/%Y/%m/%d')
    photoUploadDate = models.DateTimeField("photoUploadDate", auto_now=True, blank=True, null=True)

class Music(models.Model):
    uploadedSong = models.FileField(upload_to='uploadedSongs/%Y/%m/%d', default='uploadedSongs', blank=True)
    email = models.CharField(max_length=255)
    song_name_or_link = models.CharField(max_length=255, blank=True)
    intention = models.CharField(max_length=255, blank=True)
    musicUploadDate = models.DateTimeField("musicUploadDate", auto_now=True, blank=True, null=True)
    event = models.ForeignKey("Events", blank=True, null=True)

    def __unicode__(self):
        return self.song_name_or_link+ " : " + self.email + " : " + str(self.musicUploadDate)

class globalEvent(models.Model):
    title = models.CharField(max_length=255)
    eventPic = models.ForeignKey(Photos, unique=True)
    #start_time = models.DateTimeField("Event Time")
    arrive_start_time = models.DateTimeField("Event Start Time")
    music_start_time = models.DateTimeField("Music Start Time")


class Events(models.Model):
    title = models.CharField(max_length=100)
    start_time = models.DateTimeField("Event Time")
    arrive_start_time = models.DateTimeField("Event Start Time")
    music_start_time = models.DateTimeField("Music Start Time")
    city = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    google_map_link = models.CharField(max_length=1000)
    latitude = models.FloatField(default=40.74481)
    longitude = models.FloatField(default=-119.22230)
    eventPic = models.ForeignKey(Photos, unique=True)
    eventMix = models.ForeignKey(Music, blank=True, null=True)
    fbEvent = models.URLField(default="https://www.facebook.com/SilentDiscoSquad")
    globalEvent = models.ForeignKey(globalEvent, blank=True, null=True)

    ORGANIZER = 'organizer'
    DJ = 'dj'
    VIDEOGRAPHER = 'videographer'
    PHOTOGRAPHER = 'photographer'
    ORGANIZERCHOICES = (
        (ORGANIZER, 'organizer'),
        (DJ, 'dj'),
        (VIDEOGRAPHER, 'videographer'),
        (PHOTOGRAPHER, 'photographer'),
    )
    role1 = models.CharField(max_length=255, choices=ORGANIZERCHOICES, blank=True, null=True)
    organizer1 = models.ForeignKey("UserProfile", related_name='organizerProfile1', null=True, blank=True)
    role2 = models.CharField(max_length=255, choices=ORGANIZERCHOICES, blank=True, null=True)
    organizer2 = models.ForeignKey("UserProfile", related_name='organizerProfile2', null=True, blank=True)
    role3 = models.CharField(max_length=255, choices=ORGANIZERCHOICES, blank=True, null=True)
    organizer3 = models.ForeignKey("UserProfile", related_name='organizerProfile3', null=True, blank=True)

    def __unicode__(self):
        return self.title

class UserProfile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, unique=True)
    profilePic = models.ForeignKey(Photos)
    signupDate = models.DateTimeField("signupDate", auto_now=True)
    def __unicode__(self):
        return self.user.username
User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])


class potentialOrganizer(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    why = models.CharField(max_length=4095)

class organizerForm(ModelForm):
    class Meta:
        model = potentialOrganizer
        fields = ['name', 'email', 'city', 'why']



class MusicForm(ModelForm):
    class Meta:
        model = Music
        fields = ['email', 'song_name_or_link', 'intention', 'uploadedSong']

