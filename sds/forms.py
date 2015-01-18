from django.forms import *
from registration.forms import RegistrationForm
from sds.models import *
from myauth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserProfileForm(ModelForm):
    newsletter = forms.BooleanField(initial=True)
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields["role"].choices = [("", "Select your Role"),] + list(self.fields["role"].choices)[1:] 
        self.fields['city'].empty_label = "Select your City"

    class Meta:
        model = UserProfile 
        exclude = ['user', 'activation_key', 'key_expires', 'profilePic', 'discosAttended']
        fields = ['role', 'dancefloorSuperpower', 'city', 'zipcode', 'newsletter']

class MusicForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(MusicForm, self).__init__(*args, **kwargs)
        self.fields['uploadedSong'].label = 'Upload Song'
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

class UpdateProfile(forms.ModelForm):
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

    def clean_email(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')

        if email and User.objects.filter(email=email).exclude(username=username).count():
            raise forms.ValidationError('This email address is already in use. Please supply a different email address.')
        return email

    def save(self, commit=True):
        user = super(UpdateProfile, self).save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
        return user

class photoUploadForm(ModelForm):
    class Meta:
        model = Photos
        fields = ['user', 'photoFile', 'title']

class eventForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(eventForm, self).__init__(*args, **kwargs)
        self.fields['eventCity'].empty_label = "Select your City"
    class Meta:
        model = Events
        exclude = ['latitude', 'longitude', 'eventPic',  'organizer']
        fields = ['title', 'eventCity', 'location', 'arrive_start_time', 'eventMix', 'music_start_time', 'google_map_link', 'fbEvent', 'globalEvent', 'active']

class cityForm(ModelForm):
    class Meta:
        model = city
        exclude = ['cityImage']
        fields = ['cityName']

class uploadMix(ModelForm):
    class Meta:
        model = Music
        exclude = ['song_name_or_link', 'intention']
        fields = ['uploadedSong', 'event']    

