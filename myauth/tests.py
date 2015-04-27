from django.test import TestCase
import models as myauth_models
from django.contrib.auth import get_user_model

#from myauth.models import * 
#from django.contrib.auth.models import User

class UserTests(TestCase):
	def test_username(self):
		test_username = "user_1"
		test_user = get_user_model().objects.create_user(test_username)
		self.assertEqual(test_user.username, test_username)
	
	def test_username_from_db(self):
		test_username = "user_2"
		test_email = "user_2@test.com"
		test_user = get_user_model().objects.create_user(test_username, test_email)
		test_user.save()
		test_user_from_db = get_user_model().objects.get(username=test_username)
		self.assertEqual(test_user_from_db.username, test_username)
	
	def test_email(self):
		test_username = "user_3"
		test_email = "user_3@test.com"
		test_user = get_user_model().objects.create_user(test_username, test_email)
		test_user.save()
		test_user_from_db = get_user_model().objects.get(email=test_email)
		self.assertEqual(test_user_from_db.email, test_email)
	
	def test_password(self):
		test_username = "user_4"
		test_email = "user_4@test.com"
		test_password = "user_4_pass"
		test_user = get_user_model().objects.create_user(test_username, test_email, test_password)
		test_user.save()
		test_user_from_db = get_user_model().objects.get(email=test_email)
		self.assertTrue(test_user_from_db.check_password(test_password))

"""class UserprofileTests(TestCase):
	def test_userprofile(self):
		test_username = "some_username"
		test_user = get_user_model().objects.create_user(test_username)
		self.assertEqual(test_user.username, test_username)
"""

"""    
should write a test that checks the status status_code
when we create a new account using the form

def test_index(self):
        resp = self.client.get('/polls/')
        self.assertEqual(resp.status_code, 200)
"""

#what test cases do we need to cover?

#creating a user with an associated userprofile and sticking it in the DB