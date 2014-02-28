from django.http import HttpResponse
from django.shortcuts import *
from sds.models import Photos, Music, Events
from django.template import RequestContext, loader
from boto.s3.connection import S3Connection
from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.generic import FormView
from django.core.urlresolvers import reverse
from django.forms.models import modelformset_factory
import pprint 


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

def form(request):
    template = loader.get_template('form.html')
    context = {}
    return render(request, 'form.html', context)

def userauth(request):
    context={'user' : request.user, 'pw' : request.POST}
    return render(request, 'userauth.html/', context)


def future(request):
    MusicFormSet = modelformset_factory(Music)
    context = {}
    message = "Thanks for submitting your song!"
    if request.method == 'POST':
        formset = MusicFormSet(request.POST, request.FILES)
        if formset.is_valid():
            context = {'success': message, 'formset': formset}
            formset.save()
    else:
        formset = MusicFormSet()
        context = {'formset': formset}
    return render_to_response('index_future.html', context, context_instance=RequestContext(request))

def become(request):
    context = {}
    return render(request, 'index_join_become.html', context)

def participate(request):
    context = {}
    return render(request, 'index_join_participate.html', context)

def jointhesquad(request):
    context = {}
    return render(request, 'index_jointhesquad.html', context)

def whatissds(request):
    context = {}
    return render(request, 'index_whatissds.html', context)

def handle_uploaded_file(f):
    raise ValueError (pprint.pformat(f.name))
    with open(f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)




