from sds.settings import *
from mixpanel import Mixpanel
from myauth.models import *
from sds.models import *
from requests import request, HTTPError
from django.core.files import File
from django.core.files.storage import default_storage
import facebook, sys
#mp = Mixpanel(PROJECT_TOKEN)
 

#this is the method that is called in the pipeline. It calls some helper methods below
#mainly all it does is query the FB api and create a new userprofile filled with goodies (like prof pic!) 
def save_profile(backend, user, response, *args, **kwargs):
    if backend.name == 'facebook':
        if not userprofile_exists(user): #if there is no user profile, then populate it from Facebook
            profile_pic = get_profile_picture_from_facebook(user)
            try:
                photo_obj = Photos.objects.create(photoFile=profile_pic, user=user)
                photo_obj.save()
                userprofile = UserProfile.objects.create(user=user, profilePic=photo_obj, newsletter=False)
                userprofile.save()
            except photo_obj.DoesNotExist:
                print >> sys.stderr, "photo does not exist"
        else:
            print >> sys.stderr, "userprofile already exists"
            #mp.track(user.id,'succesful account creation');
            #print >> sys.stderr, profile.dancefloorSuperpower

#uses the FB api to get the social profile for a given user
def get_facebook_profile(user):
    social_user = user.social_auth.filter(provider='facebook',).first()
    graph = facebook.GraphAPI(social_user.extra_data['access_token'])
    return graph.get_object("me")

#Get Profile Picture, and return the file
def get_profile_picture_from_facebook(user):
    facebook_profile = get_facebook_profile(user)
    url = 'http://graph.facebook.com/{0}/picture'.format(facebook_profile['id'])
    try:
        response = request('GET', url, params={'type': 'large'})
        response.raise_for_status()
    except HTTPError:
        pass
    else:
        f = default_storage.open('{0}_social.jpg'.format(user.username), 'r+w')
        photo_file = File(f)
        photo_file.write(response.content)
        return photo_file
    return None

# A method to check whether the user profile exists already, or if we have to create it
def userprofile_exists(user):
    try:
        profile = UserProfile.objects.get(user=user)
        return True
    except UserProfile.DoesNotExist:
        return False

