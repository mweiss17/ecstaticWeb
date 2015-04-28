import sys
from sds.settings import *
from mixpanel import Mixpanel
from myauth.models import *
import facebook
#mp = Mixpanel(PROJECT_TOKEN)

def save_profile(backend, user, response, *args, **kwargs):
    try:
        profile_to_check = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        profile_to_check = None
    if backend.name == 'facebook':
        if profile_to_check is None: #then populate it from Facebook
            print >> sys.stderr, "profile to check is none"
            social_user = user.social_auth.filter(
                provider='facebook',
            ).first()
            graph = facebook.GraphAPI(social_user.extra_data['access_token'])
            profile = graph.get_object("me")
            profile = UserProfile.objects.create(user=user, newsletter=False)
            profile.save()
        else:
            print >> sys.stderr, "else"
            profile = user.get_profile()
            #mp.track(user.id,'succesful account creation');
            #print >> sys.stderr, profile.dancefloorSuperpower
