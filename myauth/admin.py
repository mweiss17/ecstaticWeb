from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from myauth.models import User
from myauth.forms import UserCreationForm, UserChangeForm

class UserAdmin(AuthUserAdmin):
	fieldsets = (
		(None, {'fields': ('username', 'password')}),
		('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
		('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
			'groups', 'user_permissions')}),
		('Important dates', {'fields': ('last_login', 'date_joined')}),
	)
	add_fieldsets = (
		(None, {'fields': ('username', 'password1', 'password2')}),
		('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
		('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
	)

	form = UserChangeForm
	add_form = UserCreationForm
	list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff')
	list_editable = ('is_active',)
	list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
	search_fields = ('username', 'email', 'first_name', 'last_name')
	ordering = ('last_name','first_name',)
admin.site.register(User, UserAdmin)