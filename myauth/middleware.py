from social.apps.django_app.middleware import SocialAuthExceptionMiddleware
from django.http import HttpResponse
from social import exceptions as social_exceptions     

class MySocialAuthExceptionMiddleware(SocialAuthExceptionMiddleware):
    def process_exception(self, request, exception):
        if hasattr(social_exceptions, exception.__class__.__name__):
            return None# HttpResponse("catched: %s" % exception)
        else:
            raise exception
