from django.forms import ModelForm
from sds.models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserProfileForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields["role"].choices = [("", "Select your Role"),] + list(self.fields["role"].choices)[1:] 
        self.fields['city'].empty_label = "Select your City (or \"I don't see my city\")"

    class Meta:
        model = UserProfile 
        exclude = ['user', 'profilePic', 'activation_key', 'key_expires']
        fields = ['role', 'dancefloorSuperpower', 'city', 'zipcode']

class MusicForm(ModelForm):
    class Meta:
        model = Music 
        fields = ['email', 'intention', 'song_name_or_link', 'uploadedSong']
        
class surveySignupsForm(ModelForm):
    class Meta:
        model = surveySignups
        fields = ['email', 'event']

class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    
    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            User._default_manager.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('duplicate_email')
    
    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.is_active = False
            user.save()
        return user

    class Meta:
        model = User
        fields = ( "username", "email", "first_name", "last_name" )

class photoUploadForm(ModelForm):
    class Meta:
        model = Photos
        fields = ['user', 'photoFile', 'title']

class eventForm(ModelForm):
    class Meta:
        model = Events
        exclude = ['latitude', 'longitude', 'eventPic', 'eventMix', 'fbEvent', 'globalEvent', 'organizer']
        fields = ['title', 'eventCity', 'location', 'arrive_start_time', 'music_start_time', 'google_map_link']

class cityForm(ModelForm):
    class Meta:
        model = city
        exclude = ['cityImage']
        fields = ['cityName']
