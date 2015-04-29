from sds.settings import *
from mixpanel import Mixpanel
from myauth.models import *
from sds.models import *
from requests import request, HTTPError
from django.core.files import File
from django.core.files.storage import default_storage
import facebook, sys
#mp = Mixpanel(PROJECT_TOKEN)
 
def save_profile_picture(graph, facebook_profile, userprofile, user):
    url = 'http://graph.facebook.com/{0}/picture'.format(facebook_profile['id'])
    try:
        response = request('GET', url, params={'type': 'large'})
        response.raise_for_status()
    except HTTPError:
        pass
    else:
        photo_file = default_storage.open('{0}_social.jpg'.format(user.username), 'r+w')
        photo_file.write(response.content)
        photo_obj = Photos.objects.create(photoFile=photo_file, user=user)
        photo_obj.save()
        print >> sys.stderr, photo_obj
        userprofile.profilePic = photo_obj
        userprofile.save()
        print >> sys.stderr, "save"


def save_profile(backend, user, response, *args, **kwargs):
    try:
        profile_to_check = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        profile_to_check = None
    if backend.name == 'facebook':
        print >> sys.stderr, "1"
        if profile_to_check is None: #then populate it from Facebook
            social_user = user.social_auth.filter(
                provider='facebook',
            ).first()
            graph = facebook.GraphAPI(social_user.extra_data['access_token'])
            facebook_profile = graph.get_object("me")
            userprofile = UserProfile.objects.create(user=user, newsletter=False)
            save_profile_picture(graph, facebook_profile, userprofile, user)
            print >> sys.stderr, "2"
        else:
            profile = user.get_profile()
            #mp.track(user.id,'succesful account creation');
            #print >> sys.stderr, profile.dancefloorSuperpower
