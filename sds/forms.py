from django import forms
from sds.models import Music

class MusicForm(forms.Form):
    email = forms.CharField(max_length=255)
    songname = forms.CharField(max_length=255)
    intention = forms.CharField(max_length=255)