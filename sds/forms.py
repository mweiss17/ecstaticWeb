from django import forms
from django.forms import ModelForm
from sds.models import Music, UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile 

class MusicForm(forms.Form):
    uploadedSong = forms.FileField(required=False)
    email = forms.CharField(max_length=255)
    songname = forms.CharField(max_length=255, required=False)
    intention = forms.CharField(max_length=255, required=False)

