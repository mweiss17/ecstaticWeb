from myauth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm as AuthUserCreationForm, UserChangeForm as AuthUserChangeForm
from django.db.models import Q
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.contrib.auth.forms import PasswordResetForm

class UserCreationForm(AuthUserCreationForm):

	class Meta:
		model = User
		## This method is defined in django.contrib.auth.form.UserCreationForm and explicitly links to auth.models.User so we need to override it
	def clean_username(self):
		username = self.cleaned_data["username"]
		try:
			User._default_manager.get(username=username)
		except User.DoesNotExist:
			return username
		raise forms.ValidationError(
			self.error_messages['duplicate_username'],
			code='duplicate_username',
		)

class UserChangeForm(AuthUserChangeForm):
		
	class Meta:
		model = User


##Here is the login form
class LoginForm(forms.Form):
	login = forms.CharField(label = 'Username or e-mail', required=True)
	password = forms.CharField(label = 'Password', widget = forms.PasswordInput, required = True)
	def clean(self):
		login = self.cleaned_data.get('login', '')
		password = self.cleaned_data.get('password', '')
		self.user = None
		users = User.objects.filter(Q(username=login)|Q(email=login))
		for user in users:
			if user.is_active and user.check_password(password):
				self.user = user
		if self.user is None:
			raise forms.ValidationError('Invalid username or password')
		return self.cleaned_data

class UserForgotPasswordForm(PasswordResetForm):
    email = forms.EmailField(required=True,max_length=254)
    class Meta:
        model = get_user_model()
        fields = ("email")