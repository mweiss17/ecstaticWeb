from sds.settings import *
from myauth.models import *
from sds.models import *
from requests import request, HTTPError
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import facebook, sys, mixpanel, datetime
mp = mixpanel.Mixpanel(PROJECT_TOKEN)

#this is the method that is called in the pipeline. It calls some helper methods below
#mainly all it does is query the FB api and create a new userprofile filled with goodies (like prof pic!) 
def save_profile(strategy, backend, user, response, *args, **kwargs):
    if backend.name == 'facebook':
        if not userprofile_exists(user): #if there is no user profile, then populate it from Facebook
            profile_pic = get_profile_picture_from_facebook(user)
            try:
                photo_obj = Photos.objects.create(photoFile=profile_pic, user=user)
                photo_obj.save()
                userprofile = UserProfile.objects.create(user=user, profilePic=photo_obj, mixpanel_distinct_id=strategy.session_get('distinct_id'), newsletter=False)
                userprofile.save()
                
                #MIXPANEL people tracking and event tracking. Must be same as in myauth views create_profile 
                people_dict = {'$username' : userprofile.user.username, '$create' : datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p"), '$email' : userprofile.user.email, 'city' : "none",}
                if userprofile.city:
                    people_dict['city'] = userprofile.city.cityName
                if userprofile.user.first_name:
                    people_dict['$first_name'] = userprofile.user.first_name
                if userprofile.user.last_name:
                    people_dict['$last_name'] = userprofile.user.last_name     
                mp.track(userprofile.user.id,'signup');
                mp.track(userprofile.user.id,'login');
                mp.alias(userprofile.user.id, userprofile.mixpanel_distinct_id)
                mp.people_set(userprofile.user.id, people_dict)

            except Exception as e:
                print >> sys.stderr, '%s (%s)' % (e.message, type(e))
        else:
            print >> sys.stderr, "userprofile already exists"

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
        return file_content
    return None

# A method to check whether the user profile exists already, or if we have to create it
def userprofile_exists(user):
    try:
        profile = UserProfile.objects.get(user=user)
        print >> sys.stderr, "profile exists!!!"
        mp.track(user.id,'login');
        return True
    except UserProfile.DoesNotExist:
        print >> sys.stderr, "profile doesn't exists!!!"
        return False

