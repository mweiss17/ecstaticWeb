from django import forms
from django.forms import ModelForm
from sds.models import Music, potentialOrganizer

class MusicForm(forms.Form):
    uploadedSong = forms.FileField(required=False)
    email = forms.CharField(max_length=255)
    songname = forms.CharField(max_length=255, required=False)
    intention = forms.CharField(max_length=255, required=False)

class organizerForm(forms.Form):
    name = forms.CharField(max_length=100, required=False)
    email = forms.CharField(max_length=255)
    city = forms.CharField(max_length=255, required=False)
    why = forms.CharField(max_length=255, required=False)
