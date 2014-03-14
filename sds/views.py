from django.http import HttpResponse
from django.shortcuts import *
from sds.models import Photos, Music, Events, potentialOrganizer
from django.template import RequestContext, loader
from boto.s3.connection import S3Connection
from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.generic import FormView
from django.core.urlresolvers import reverse
from django.forms import ModelForm
from django.forms.models import modelform_factory
from sds.forms import MusicForm, organizerForm
from django.core.mail import send_mail
import pprint 
import datetime, time




def home(request):
	return render_to_response('sds.html', {})

def index(request):
    now = calculateCurrentTime()
    upcomingEvents = Events.objects.filter(start_time__gte=datetime.datetime.now()-datetime.timedelta(seconds=3600*5))
    previousEvents = Events.objects.filter(start_time__lte=datetime.datetime.now()-datetime.timedelta(seconds=3600*5))

    etaList = []
    upcomingEventsList = []
    template = loader.get_template('index.html')
    for event in upcomingEvents:
        eventstart = event.start_time
        eventstart = time.mktime(eventstart.timetuple())
        etaList.append(eventstart-now)
        upcomingEventsList.append(event.id)

    context = RequestContext(request, {
        'upcomingEvents': upcomingEvents, 'etaList': etaList, 'upcomingEventsList': upcomingEventsList, 'previousEvents': previousEvents
    })
    return HttpResponse(template.render(context))

def future(request):
    MusicForm = modelform_factory(Music, fields=("email", "songname", "intention", "uploadedSong"))
    message = "Upload a song!"
    if request.method == 'POST':
        form = MusicForm(request.POST, request.FILES)
        send_mail('Thanks for co-creating the mix!', 'Here is the message.', 'us@silentdiscosquad.com', [request.POST["email"]], fail_silently=False)
        if form.is_valid():
            message = "Thanks for submitting your song!"
            handle_uploaded_file(request.FILES['uploadedSong'])
            form.save()
    else:
        form = MusicForm()
    
    now = calculateCurrentTime()

    event = Events.objects.filter(title=request.GET['title'])
    event = event[0]
    eventstart = event.start_time
    eventstart = time.mktime(eventstart.timetuple())
    upcomingEventsList = []
    upcomingEventsList.append(event.id)

    etaList = []
    etaList.append(eventstart - now)

    context = {'success': message, 'form': form, 'event': event, 'etaList': etaList, 'upcomingEventsList': upcomingEventsList}
    return render_to_response('index_future.html', context, context_instance=RequestContext(request))

def past(request):
    event = Events.objects.filter(title=request.GET['title'])
    event = event[0]
    context = {'event': event}
    return render(request, 'index_past.html', context)

def become(request):
    OrganizerForm = modelform_factory(potentialOrganizer, fields=("name", "email", "city", "why"))
    if request.method == 'POST':
        form = OrganizerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    else:
        form = OrganizerForm()
    context = {'form': form}
    return render(request, 'index_join_become.html', context)

def form(request):
    template = loader.get_template('form.html')
    context = {}
    return render(request, 'form.html', context)

def userauth(request):
    context={'user' : request.user, 'pw' : request.POST}
    return render(request, 'userauth.html/', context)

def participate(request):
    context = {}
    return render(request, 'index_join_participate.html', context)

def jointhesquad(request):
    context = {}
    return render(request, 'index_jointhesquad.html', context)

def whatissds(request):
    context = {}
    return render(request, 'index_whatissds.html', context)

def stream(request):
    event = Events.objects.filter(title=request.GET['title'])
    event = event[0]

    now = calculateCurrentTime()

    eventstart = event.start_time
    eventstart = time.mktime(eventstart.timetuple())
    eta = eventstart - now
    eta = -eta
    context = {'event': event, 'eta': eta}
    return render(request, 'stream.html', context)

def handle_uploaded_file(f):
    with open("/home/ec2-user/sds/media/"+f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)



def calculateCurrentTime():
    now = datetime.datetime.utcnow()
    now = time.mktime(now.timetuple()) 
    now = now - 5 * 3600
    return now

