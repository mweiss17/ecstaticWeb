from django.db import models
from django.utils import timezone
from django.core import validators
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django import forms
import re, uuid, sys

class UserManager(BaseUserManager):

	def _create_user(self, username, email, password, is_staff, is_superuser, **extra_fields):
		now = timezone.now()
		if not username:
			raise ValueError(_('The given username must be set'))
		email = self.normalize_email(email)
		user = self.model(username=username, email=email,
			is_staff=is_staff, is_active=True,
			is_superuser=is_superuser, last_login=now,
			date_joined=now, **extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_user(self, username, email=None, password=None, **extra_fields):
		return self._create_user(username, email, password, False, False, **extra_fields)

	def create_superuser(self, username, email, password, **extra_fields):
		user=self._create_user(username, email, password, True, True,
		**extra_fields)
		user.is_active=True
		user.save(using=self._db)
		return user

class User(AbstractBaseUser, PermissionsMixin):
	username = models.CharField(_('username'), max_length=30, unique=True,
		help_text=_('Required. 30 characters or fewer. Letters, numbers and @/./+/-/_ characters'),
		validators=[validators.RegexValidator(re.compile('^[\w.@+-]+$'), _('Enter a valid username.'), _('invalid'))])
	first_name = models.CharField(_('first name'), max_length=30, blank=True, null=True)
	last_name = models.CharField(_('last name'), max_length=30, blank=True, null=True)
	email = models.EmailField(_('email address'), max_length=255)
	is_staff = models.BooleanField(_('staff status'), default=False,
		help_text=_('Designates whether the user can log into this admin site.'))
	is_active = models.BooleanField(_('active'), default=True,
		help_text=_('Designates whether this user should be treated as active. Unselect this instead of deleting accounts.'))
	date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
	objects =  UserManager()

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email',]
	class Meta:
		verbose_name = _('user')
		verbose_name_plural = _('users')

	def get_full_name(self):
		full_name = '%s %s' % (self.first_name, self.last_name)
		return full_name.strip()

	def get_short_name(self):
		return self.first_name

	def get_profile(self):
		return property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

	def email_user(self, subject, message, from_email=None):
		send_mail(subject, message, from_email, [self.email])

class UserProfile(models.Model):
    #Role
    ORGANIZER = 'Organizer'
    DJ = 'DJ'
    VIDEOGRAPHER = 'Videographer'
    PHOTOGRAPHER = 'Photographer'
    DANCER = 'Dancer'
    ORGANIZERCHOICES = (
        (ORGANIZER, 'Organizer'),
        (DJ, 'DJ'),
        (VIDEOGRAPHER, 'Videographer'),
        (PHOTOGRAPHER, 'Photographer'),
        (DANCER, 'Dancer'),
    )
    role = models.CharField(max_length=255, choices=ORGANIZERCHOICES, blank=True, null=True)

    #Other Fields
    city = models.ForeignKey("sds.city", blank=True, null=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile')
    profilePic = models.ForeignKey("sds.Photos", blank=True, null=True)
    signupDate = models.DateTimeField("signupDate", auto_now=True)
    dancefloorSuperpower = models.CharField(max_length=2048, blank=True, null=True)
    zipcode = models.CharField(max_length=10, default=00000, blank=True, null=True)
    newsletter = models.BooleanField()
    mixpanel_distinct_id = models.CharField(max_length=100, blank=True, null=True)
    def __unicode__(self):
        return self.user.username
User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

