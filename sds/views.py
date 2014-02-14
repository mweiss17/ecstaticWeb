from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from sds.models import Photos
from django.template import RequestContext, loader
from boto.s3.connection import S3Connection
from django.shortcuts import render
from django.contrib.auth.models import User


def test(request):
    latest_poll_list = Photos.objects.filter(user_id="martin")
    template = loader.get_template('test.html')
    context = {'latest_poll_list': latest_poll_list}
    return render(request, 'test.html', context)

def home(request):
	return render_to_response('sds.html', {})

def index(request):
    latest_poll_list = Photos.objects.filter(user_id="martin")
    template = loader.get_template('index.html')
    context = RequestContext(request, {
        'latest_poll_list': latest_poll_list,
    })
    return HttpResponse(template.render(context))

	#conn = S3Connection('<AKIAIC27KBAMV4JLB2CQ>', '<sCJ4UkJ4kBszPymJeLxmeTj6H6UmY8zrL0uvOa9+>')
	#bucket = conn.create_bucket('mybucket')

def form(request):
    template = loader.get_template('form.html')
    context = {}
    return render(request, 'form.html', context)

def userauth(request):
#    auth = get_object_or_404(User, pk=1)
    context={'user' : request.user, 'pw' : request.POST}
    return render(request, 'userauth.html/', context)


