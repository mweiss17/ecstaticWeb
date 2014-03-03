from django.http import HttpResponse
from django.shortcuts import *
from sds.models import Photos, Music, Events
from django.template import RequestContext, loader
from boto.s3.connection import S3Connection
from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.generic import FormView
from django.core.urlresolvers import reverse
from django.forms import ModelForm
from django.forms.models import modelform_factory
from sds.forms import MusicForm
import pprint 
import datetime, time




def home(request):
	return render_to_response('sds.html', {})

def index(request):
    upcomingEvents = Events.objects.all()
    etaList = []
    upcomingEventsList = []
    template = loader.get_template('index.html')
    for event in upcomingEvents:
        now = datetime.datetime.utcnow()
        now = time.mktime(now.timetuple()) 
        now = now - 5 * 3600

        eventstart = event.start_time
        eventstart = time.mktime(eventstart.timetuple())
        etaList.append(eventstart-now)
        upcomingEventsList.append(event.id)

    context = RequestContext(request, {
        'upcomingEvents': upcomingEvents, 'etaList': etaList, 'upcomingEventsList': upcomingEventsList
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
    MusicForm = modelform_factory(Music, fields=("email", "songname", "intention", "uploadedSong"))
    event = Events.objects.filter(title=request.GET['title'])
    event = event[0]
    if request.method == 'POST':
        form = MusicForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['uploadedSong'])
            form.save()
    else:
        form = MusicForm()
    message = "Thanks for submitting your song!"
    
    now = datetime.datetime.utcnow()
    now = time.mktime(now.timetuple()) 
    now = now - 5 * 3600

    eventstart = event.start_time
    eventstart = time.mktime(eventstart.timetuple())
    eta = eventstart - now

    context = {'success': message, 'form': form, 'event': event, 'eta': eta}
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
    with open("/home/ec2-user/sds/media/"+f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)




