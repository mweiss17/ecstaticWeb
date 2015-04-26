from django.test import TestCase
import models as myauth_models
from django.contrib.auth import get_user_model

#from myauth.models import * 
#from django.contrib.auth.models import User

class UserTests(TestCase):
	def test_username(self):
		test_username = "some_username"
		test_user = get_user_model().objects.create_user(test_username)
		self.assertEqual(test_user.username, test_username)


"""    
should write a test that checks the status status_code
when we create a new account using the form

def test_index(self):
        resp = self.client.get('/polls/')
        self.assertEqual(resp.status_code, 200)
"""