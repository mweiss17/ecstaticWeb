from django import forms
from django.forms import ModelForm
from sds.models import Music

class MusicForm(forms.Form):
    uploadedSong = forms.FileField()
    email = forms.CharField(max_length=255)
    songname = forms.CharField(max_length=255)
    intention = forms.CharField(max_length=255)
