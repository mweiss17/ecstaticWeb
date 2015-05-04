from sds.settings import *
from myauth.models import *
from sds.models import *
from requests import request, HTTPError
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import facebook, sys, mixpanel
 

#this is the method that is called in the pipeline. It calls some helper methods below
#mainly all it does is query the FB api and create a new userprofile filled with goodies (like prof pic!) 
def save_profile(backend, user, response, *args, **kwargs):
    mp = mixpanel.Mixpanel(PROJECT_TOKEN)
    if backend.name == 'facebook':
        if not userprofile_exists(user): #if there is no user profile, then populate it from Facebook
            profile_pic = get_profile_picture_from_facebook(user)
            try:
                photo_obj = Photos.objects.create(photoFile=profile_pic, user=user)
                photo_obj.save()
                userprofile = UserProfile.objects.create(user=user, profilePic=photo_obj, newsletter=False)
                userprofile.save()
            except Exception as e:
                print >> sys.stderr, '%s (%s)' % (e.message, type(e))
        else:
            print >> sys.stderr, "userprofile already exists"
            #mp.track(user.id,'succesful account creation');
            #mp.alias(userObj.pk, userProfileObj.mixpanel_distinct_id)
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
    print >> sys.stderr, url
    try:
        response = request('GET', url, params={'type': 'large'})
        response.raise_for_status()
    except HTTPError:
        print >> sys.stderr, "httperror!!!"
        pass
    else:
        file_content = ContentFile(response.content)
        #f = default_storage.open('{0}_social.jpg'.format(user.username), 'r+')
        #f.write(response.content)
        #f.close()
        return file_content
    return None

# A method to check whether the user profile exists already, or if we have to create it
def userprofile_exists(user):
    try:
        profile = UserProfile.objects.get(user=user)
        print >> sys.stderr, "profile exists!!!"
        return True
    except UserProfile.DoesNotExist:
        print >> sys.stderr, "profile doesn't exists!!!"
        return False

