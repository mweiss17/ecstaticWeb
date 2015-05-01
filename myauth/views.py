from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.views.generic.edit import FormView
from django.contrib.auth import login
from myauth.forms import LoginForm
from sds.forms import *
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from myauth.forms import *
from sds.models import *
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib import auth
from django.conf import settings
from sds.settings import *
from mailchimp import utils
import logging, json, pprint, datetime, time, hashlib,random,sys,socket, mixpanel
mp = mixpanel.Mixpanel(PROJECT_TOKEN)

def addloginform(context):
	loginform = LoginForm()
	loginform.fields['login'].widget.attrs['class'] = "submit-track user-login"
	loginform.fields['login'].widget.attrs['placeholder'] = "Disco-Name"
	loginform.fields['password'].widget.attrs['class'] = "submit-track user-login"
	loginform.fields['password'].widget.attrs['placeholder'] = "Password"
	context.update({'loginform':loginform})
	return

def forgotpassword(request):
	cities = city.objects.filter()
	context = {'cities':cities}
	addloginform(context)
	ufpr = UserForgotPasswordForm()

	if request.method == 'POST':
		ufpr = UserForgotPasswordForm(request.POST)
		context.update({'ufpr':ufpr})
		if ufpr.is_valid():
			User = get_user_model()
			user = User.objects.filter(email=request.POST['email'])
			user.backend = 'django.contrib.auth.backends.ModelBackend'
			if user and settings.SITE_ID == 5:
				ufpr.save(from_email='Martin@SilentDiscoSquad.com', email_template_name='myauth/DEVELOPMENT_password_reset_email.html')
				context.update({'success':"success"})
				return render(request, 'forgotpassword.html', context)
			elif user and settings.SITE_ID == 2:
				ufpr.save(from_email='Martin@SilentDiscoSquad.com', email_template_name='myauth/password_reset_email.html')
				context.update({'success':"success"})
				return render(request, 'forgotpassword.html', context)
			else:
				messages.error(request, 'We couldn\'t find any accounts with that email. Give it another shot?')
				return render(request, 'forgotpassword.html', context)
	context.update({'ufpr':ufpr})
	return render(request, 'forgotpassword.html', context)

def loginView(request):
	User = get_user_model()
	name = request.POST['login']
	password = request.POST['password']
	users = User.objects.filter(Q(username=name)|Q(email=name))
	context = {}
	for user in users:
		if user.check_password(password):
			user.backend = 'django.contrib.auth.backends.ModelBackend'
			auth.login(request, user)
			context.update({'successful_login': True})
			return HttpResponseRedirect(request.META.get('HTTP_REFERER'), context)
	messages.error(request, 'Incorrect username or password, try again.')
	return HttpResponseRedirect(request.META.get('HTTP_REFERER')+"#login", context)

	## Want to modify this such that if you get a GET request with a username, you load THAT user, but you 
## don't allow the other user to modify their shiz.
def profile(request):
	context = {}
	username = request.GET.get('username', '')
	if username != '':
		currentUserProfile = UserProfile.objects.get(user=User.objects.get(username=username))
		context.update({"myprofile":False})
	else:
		currentUserProfile = UserProfile.objects.get(user=request.user)
		context.update({"myprofile":True})

	context.update({'currentUserProfile':currentUserProfile})

	pf = photoUploadForm(instance=currentUserProfile.profilePic)
	uf = profile_update_form(instance=currentUserProfile.user)
	upf = UserProfileForm(instance=currentUserProfile)
	context.update({"uf" : uf, "upf" : upf, "pf":pf})
	return render(request, 'profile.html', context)

def profileupdate(request):
	context = {}
	context.update({"myprofile":True})
	pf = photoUploadForm(request.POST, request.FILES, instance=request.user.profile.profilePic)
	uf = profile_update_form(data=request.POST, instance=request.user)
	upf = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)
	context.update({'uf':uf, 'upf':upf, 'pf':pf})

	if uf.is_valid():
		userObj = uf.save()
		if pf.is_valid():                 
			photoObj = pf.save(commit=False)
			photoObj.user = userObj
			photoObj.save()
		if upf.is_valid() and not pf.is_valid():
			userProfileObj = upf.save(commit=False)
			userProfileObj.user = userObj
			userProfileObj.save()
		elif upf.is_valid():
			userProfileObj = upf.save(commit=False)
			userProfileObj.user = userObj
			userProfileObj.profilePic = photoObj
			userProfileObj.save()
	context.update({"uf" : uf, "upf" : upf, "pf":pf, 'currentUserProfile':UserProfile.objects.get(user=request.user)})
	return render(request, 'profile.html', context)


def createprofile(request):
	context = {}
	if request.method == 'POST':
		uf = UserCreateForm(request.POST, request.FILES)
		upf = UserProfileForm(request.POST, request.FILES)
		pf = photoUploadForm(request.POST, request.FILES)
		context.update({'uf': uf, 'upf':upf, 'pf':pf})
		profile_CSS(uf, upf)
		if uf.is_valid() and upf.is_valid() and pf.is_valid():
			userObj = uf.save()
			userProfileObj = upf.save(commit=False)
			userProfileObj.user = userObj
			photoObj = pf.save(commit=False)
			photoObj.user = userObj
			photoObj.save()
			context.update({'pf':photoObj})
			userProfileObj.profilePic = photoObj
			email = uf.cleaned_data['email']
			salt = hashlib.sha1(str(random.random())).hexdigest()[:5]            
			userProfileObj.save()
			context.update({'upf': userProfileObj})
			if upf.cleaned_data['newsletter']:
				subscribeToMailchimp(email)
			userObj.backend = 'django.contrib.auth.backends.ModelBackend'
			auth.login(request, userObj)
			people_dict = {'$username' : userObj.username, '$create' : datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p"), '$email' : email, 'city' : "none",}
			if userProfileObj.city:
				people_dict['city'] = userProfileObj.city.cityName
			if userObj.first_name:
				people_dict['$first_name'] = userObj.first_name
			if userObj.last_name:
				people_dict['$last_name'] = userObj.last_name            
			mp.alias(userObj.pk, userProfileObj.mixpanel_distinct_id)
			mp.people_set(userObj.pk, people_dict)

			return render(request, 'register_success.html', context)
		return render(request, 'createprofile.html', context)

	else:
		pf = photoUploadForm()
		uf = UserCreateForm()
		upf = UserProfileForm()
		profile_CSS(uf, upf)
		context.update({"uf" : uf, "upf" : upf, "pf":pf})
		context.update({"createprofile":True})
		return render(request, 'createprofile.html', context)

def profile_CSS(uf, upf):
	uf.fields['first_name'].widget.attrs['class'] = "formstyle"
	uf.fields['last_name'].widget.attrs['class'] = "formstyle"
	uf.fields['username'].widget.attrs['class'] = "formstyle"
	uf.fields['email'].widget.attrs['class'] = "formstyle"
	uf.fields['password1'].widget.attrs['class'] = "formstyle"
	uf.fields['password2'].widget.attrs['class'] = "formstyle"
	uf.fields['first_name'].widget.attrs['placeholder'] = "First Name"
	uf.fields['last_name'].widget.attrs['placeholder'] = "Last Name"
	uf.fields['username'].widget.attrs['placeholder'] = "Disco Name"
	uf.fields['email'].widget.attrs['placeholder'] = "E-mail"
	uf.fields['password1'].widget.attrs['placeholder'] = "Password"
	uf.fields['password2'].widget.attrs['placeholder'] = "Password (repeat)"
	upf.fields['role'].widget.attrs['class'] = "formstyle"
	upf.fields['dancefloorSuperpower'].widget.attrs['class'] = "formstyle"
	upf.fields['city'].widget.attrs['class'] = "formstyle"
	upf.fields['zipcode'].widget.attrs['class'] = "formstyle"
	upf.fields['role'].widget.attrs['placeholder'] = "Role"
	upf.fields['dancefloorSuperpower'].widget.attrs['placeholder'] = "Dancefloor Superpower"
	upf.fields['city'].widget.attrs['placeholder'] = "What city do you live closest to?"
	upf.fields['zipcode'].widget.attrs['placeholder'] = "zipcode"
	upf.fields['mixpanel_distinct_id'].widget.attrs['id'] = "mixpanel_distinct_id"
	upf.fields['mixpanel_distinct_id'].widget.attrs['class'] = "hidden"
	return

def subscribeToMailchimp(email):
	try:
		list = utils.get_connection().get_list_by_id(MAILCHIMP_LIST_ID)
		list.subscribe(email, {'EMAIL': email})
	except:
		pass


