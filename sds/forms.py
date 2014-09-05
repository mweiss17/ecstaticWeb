from django import forms
from django.forms import ModelForm
from sds.models import *
from django.contrib.auth.models import User

class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile 
        fields = ['role', 'user', 'profilePic', 'dancefloorSuperpower']

class MusicForm(ModelForm):
    class Meta:
        model = Music 
        fields = ['email', 'intention', 'song_name_or_link', 'uploadedSong']
        
class surveySignupsForm(ModelForm):
    class Meta:
        model = surveySignups
        fields = ['email', 'event']


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput)

    class Meta:
        model = User
        # Note - include all *required* CustomUser fields here,
        # but don't need to include password1 and password2 as they are
        # already included since they are defined above.
        fields = ("username",)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            msg = "Passwords don't match"
            raise forms.ValidationError("Password mismatch")
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class ReadOnlyPasswordHashWidget(forms.Widget):
    def render(self, name, value, attrs):
        encoded = value
        final_attrs = self.build_attrs(attrs)
        if not encoded or encoded.startswith(UNUSABLE_PASSWORD_PREFIX):
            summary = mark_safe("<strong>%s</strong>" % ugettext("No password set."))
        else:
            try:
                hasher = identify_hasher(encoded)
            except ValueError:
                summary = mark_safe("<strong>%s</strong>" % ugettext("Invalid password format or unknown hashing algorithm."))
            else:
                summary = format_html_join('',
                "<strong>{0}</strong>: {1} ",
                ((ugettext(key), value)
                for key, value in hasher.safe_summary(encoded).items())
                )
        return format_html("<div{0}>{1}</div>", flatatt(final_attrs), summary)

class ReadOnlyPasswordHashField(forms.Field):
    widget = ReadOnlyPasswordHashWidget

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("required", False)
        super(ReadOnlyPasswordHashField, self).__init__(*args, **kwargs)
    
    def bound_data(self, data, initial):
        # Always return initial because the widget doesn't
        # render an input field.
        return initial
    
    def has_changed(self, initial, data):
        return False

class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()
    class Meta:
        model = User
    def clean_password(self):
        return self.initial['password']


