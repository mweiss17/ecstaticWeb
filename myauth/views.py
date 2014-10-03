from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.views.generic.edit import FormView
from django.contrib.auth import login
from myauth.forms import LoginForm
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from myauth.forms import *
from sds.models import *
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib import auth

def forgotpassword(request):
	context = {}
	ufpr = UserForgotPasswordForm()
	if request.method == 'POST':
		ufpr = UserForgotPasswordForm(request.POST)
		if ufpr.is_valid():
			ufpr.save(from_email='Martin@SilentDiscoSquad.com', email_template_name='myauth/password_reset_email.html')
	context.update({'ufpr':ufpr})
	return render(request, 'forgotpassword.html', context)


def loginView(request):
	User = get_user_model()
	name = request.POST['login']
	password = request.POST['password']
	users = User.objects.filter(Q(username=name)|Q(email=name))
	context = {}
	for user in users:
		if user.is_active and user.check_password(password):
			user.backend = 'django.contrib.auth.backends.ModelBackend'
			auth.login(request, user)
			return HttpResponseRedirect(request.META.get('HTTP_REFERER'), context)
	messages.error(request, 'Incorrect username or password, try again.')
	return HttpResponseRedirect(request.META.get('HTTP_REFERER')+"#login", context)
