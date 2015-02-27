from django.http import HttpResponse
from django.shortcuts import *
from sds.models import *
from django.template import RequestContext, loader
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.generic import FormView
from django.core.urlresolvers import reverse
from django.forms import ModelForm
from django.forms.models import modelform_factory
from sds.forms import *
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from settings import *
from django.contrib import auth
from django.core.context_processors import csrf
from mailchimp import utils
from django.contrib.auth.forms import *
from django.contrib import messages
from myauth.forms import *
from django.contrib.auth import login
import logging, json, pprint, datetime, time, hashlib, random,sys,mixpanel
mp = mixpanel.Mixpanel(PROJECT_TOKEN)
#print >> sys.stderr, mySubString

def calculateCurrentTime():
    now = datetime.datetime.utcnow()
    now = time.mktime(now.timetuple()) 
    return now

def create_login_form():
    loginform = LoginForm()
    loginform.fields['login'].widget.attrs['class'] = "submit-track user-login"
    loginform.fields['login'].widget.attrs['placeholder'] = "Disco-Name"
    loginform.fields['password'].widget.attrs['class'] = "submit-track user-login"
    loginform.fields['password'].widget.attrs['placeholder'] = "Password"
    return loginform

def common_context(request):
    context = {}
    context.update({'cities':city.objects.filter()})
    context.update({'loginform':create_login_form()})
    context.update({'PROJECT_TOKEN':PROJECT_TOKEN})
    context.update({'upcomingEvents':Events.objects.filter(arrive_start_time__gte=datetime.datetime.now()-datetime.timedelta(seconds=3600*3))})
    return context

def index(request):
    return render(request, 'index.html', {})

def about(request):
    return render(request, 'about.html', {})

def organize(request):
    context = {}
    if request.method == 'POST':
        ef = eventForm(request.POST)
        pf = photoUploadForm(request.POST, request.FILES)
        cf = cityForm(request.POST)
        cpf = photoUploadForm(request.POST, request.FILES)
        um = uploadMix(request.POST, request.FILES)
        context.update({'ef':ef, 'pf':pf, 'cf':cf, 'cpf':cpf, 'um':um})
        if pf.is_valid():      
            photoObj = pf.save(commit=False)
            photoObj.user = request.user
            photoObj.save()            
        if ef.is_valid():
            eventObject = ef.save(commit=False)
            s = eventObject.google_map_link
            mySubString=s[s.find("\"")+1:s.find("\"")]
            eventObject.google_map_link = mySubString
            eventObject.eventPic = photoObj
            eventObject.organizer = request.user
            if cf.is_valid() and cpf.is_valid() and eventObject.eventCity is None:
                cityPhotoObject = cpf.save(commit=False)
                cityPhotoObject.user = request.user
                cityPhotoObject.save()
                cityObject = cf.save(commit=False)
                cityObject.cityImage = cityPhotoObject.photoFile
                cityObject.save()
                eventObject.eventCity = cityObject
                eventObject.active = False
            if um.is_valid():
                mix = um.save(commit=False)
                mix.event = eventObject
                mix.save()
                eventObject.eventMix = mix
            eventObject.save()
            email_subject = 'SDS Event Confirmation'
            email_body = "Hello Disco Organizer!\n\nNice - you just created an event; our team is verifying all the information you gave us. Once we approve your event we will reach out to you. Approval should be within a few hours.\n\nThanks for Turning the World into a Dancefloor!\n\nWith a Smile,\n\nThe SDS Team" 
            send_mail(email_subject, email_body, 'david@silentdiscosquad.com', [request.user.email], fail_silently=False)
            return render(request, 'event_creation_success.html', context)
        else:
            return render(request, 'organize.html', context)
    else:
        ef = eventForm()
        pf = photoUploadForm()
        cf = cityForm()
        cpf = photoUploadForm()
        um = uploadMix()

        ef.fields['title'].widget.attrs['class'] = "formstyle"
        ef.fields['eventCity'].widget.attrs['class'] = "formstyle"
        ef.fields['location'].widget.attrs['class'] = "formstyle"
        ef.fields['google_map_link'].widget.attrs['class'] = "formstyle"
        ef.fields['fbEvent'].widget.attrs['class'] = "formstyle"
        ef.fields['arrive_start_time'].widget.attrs['class'] = "formstyle"
        ef.fields['music_start_time'].widget.attrs['class'] = "formstyle"
        ef.fields['globalEvent'].widget.attrs['class'] = "formstyle"
        cf.fields['cityName'].widget.attrs['class'] = 'formstyle'

        ef.fields['title'].widget.attrs['placeholder'] = "Title of the Event"
        ef.fields['arrive_start_time'].widget.attrs['placeholder'] = "When does the event begin?"
        ef.fields['music_start_time'].widget.attrs['placeholder'] = "When does the mix begin?"
        ef.fields['eventCity'].widget.attrs['placeholder'] = "City"
        ef.fields['location'].widget.attrs['placeholder'] = "Specific Location"
        ef.fields['google_map_link'].widget.attrs['placeholder'] = "Google Maps Link"
        ef.fields['fbEvent'].widget.attrs['placeholder'] = "Facebook Event Link"

        ef.fields['arrive_start_time'].widget.attrs['data-format'] = "MM/dd/yyyy hh:mm"
        ef.fields['music_start_time'].widget.attrs['data-format'] = "MM/dd/yyyy hh:mm"

        cf.fields['cityName'].widget.attrs['placeholder'] = 'My City\'s Name'

        context.update({"upcomingEvents":upcomingEvents, "ef":ef, "pf":pf, "cf":cf, "cpf":cpf,'um':um})
        return render(request, 'organize.html', context)

def event_creation_success(request):
    return render(request, 'event_creation_success.html', {})

def register_success(request):
    return render_to_response('register_success.html')

def process_song_submission(request):
    form = MusicForm(request.POST, request.FILES)
    send_mail('Dancetrack Received', "We got your track! Thanks for your contribution to the Dancemix \nWith Love," +"\nThe SDS Team", 'us@silentdiscosquad.com', [request.POST["email"]], fail_silently=False)            
    send_mail("Received Track from: "+ request.POST['email'], "songname: "+ request.POST['song_name_or_link'] + " intention: "+ request.POST['intention'],'contact@silentdiscosquad.com', ['david@silentdiscosquad.com'], fail_silently=False)       
    if form.is_valid():
        message = "Thanks for submitting your song!"
        form.save()
    return form

def format_song_upload_form(form):
    form.fields['uploadedSong'].widget.attrs['id'] = "fileToUpload"
    form.fields['uploadedSong'].widget.attrs['label'] = "Upload Song"
    form.fields['uploadedSong'].widget.attrs['onchange'] = "fileSelected()"
    form.fields['song_name_or_link'].widget.attrs['class'] = "formstyle"
    form.fields['intention'].widget.attrs['class'] = "formstyle"
    form.fields['email'].widget.attrs['placeholder'] = "Email"
    form.fields['email'].widget.attrs['class'] = "formstyle"
    form.fields['song_name_or_link'].widget.attrs['placeholder'] = "Songname"
    form.fields['intention'].widget.attrs['placeholder'] = "Intention"


def future(request):
    context = {}
    event = Events.objects.get(id=request.GET['id'])
    organizer = UserProfile.objects.get(user=event.organizer)
    context.update({'event' : event})
    context.update({"organizer":organizer})
    if request.method == 'POST':
        form = process_song_submission(request)
    else:
        form = MusicForm()
    context.update({"form":form})
    format_song_upload_form(form)
    return render(request, 'future.html', context)

def citypage_city(request):
    context = {}
    upcomingEvents = Events.objects.filter(arrive_start_time__gte=datetime.datetime.now()-datetime.timedelta(seconds=3600*7), eventCity=city.objects.get(cityName=str(request.GET['city'])), active=True)
    community = UserProfile.objects.filter(city=city.objects.get(cityName=str(request.GET['city']))).exclude(profilePic__photoFile="")
    context.update({"upcomingEvents":upcomingEvents, "community":community, "eventCity":str(request.GET['city'])})
    return render(request, 'citypage_city.html', context)

def contact(request):
    context = {}
    if request.method == 'POST':
            send_mail("From: "+request.POST['email']+" "+request.POST['subject'], request.POST['message'], "contact@silentdiscosquad.com" , ['martin@silentdiscosquad.com', 'david@silentdiscosquad.com'])
    return render(request, 'contact.html', context)

def stream(request):
    cities = city.objects.filter()
    event = Events.objects.filter(id=request.GET['id'])
    event = event[0]

    eventstart = event.music_start_time
    eventstart = time.mktime(eventstart.timetuple())
    eta = eventstart - calculateCurrentTime()
    eta = -eta
    context = {'event': event, 'eta': eta, "cities":cities}
    try:
        if(request.GET['async']):
            return HttpResponse(eta)
    except Exception, e:
        pass
    return render(request, 'stream.html', context)



def handle_uploaded_file(f):
    with open("/home/ec2-user/sds/media/"+f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def appindex(request):
    TimeZone = datetime.timedelta(seconds=3600*7) #adjustment for EST (4 hrs) + 
                                                  #adjustment for inprogress events (3 hours)
    upcomingEvents = Events.objects.filter(arrive_start_time__gte=datetime.datetime.now()-TimeZone)
    previousEvents = Events.objects.filter(arrive_start_time__lte=datetime.datetime.now()-datetime.timedelta(seconds=3600*4))
    upcomingGlobalEvent = globalEvent.objects.filter(arrive_start_time__gte=datetime.datetime.now()-TimeZone)

    future = 'False'
    etaList = []
    upcomingEventsList = []

    some_data_to_dump = []
    for event in upcomingEvents:
        eventstart = event.music_start_time
        eventstart = time.mktime(eventstart.timetuple())
        etaList.append(eventstart-calculateCurrentTime())
        upcomingEventsList.append(event.id)
        if event.eventMix:
            some_data_to_dump.append({'id': event.id, 'title': event.title, 'start':eventstart, 'city': event.eventCity.cityName, 'location':event.location, 'map':event.google_map_link, 'fbevent':event.fbEvent, 'latitude':event.latitude, 'longitude':event.longitude, 'songTitle':event.eventMix.uploadedSong.url})
        else:
            some_data_to_dump.append({'id': event.id, 'title': event.title, 'start':eventstart, 'city': event.eventCity.cityName, 'location':event.location, 'map':event.google_map_link, 'fbevent':event.fbEvent, 'latitude':event.latitude, 'longitude':event.longitude, 'songTitle':"No Mix Uploaded!"})

    data = json.dumps(some_data_to_dump)

    context = RequestContext(request, {
        'future': future, 'upcomingEvents': upcomingEvents, 'etaList': etaList, 'upcomingEventsList': upcomingEventsList, 'previousEvents': previousEvents
    })
    return HttpResponse(data, mimetype='application/json')
        
def logout(request):
    auth.logout(request)
    context = {}
    if "profile.html" in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect('/')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def subscribeToMailchimp(email):
    try:
        list = utils.get_connection().get_list_by_id(MAILCHIMP_LIST_ID)
        list.subscribe(email, {'EMAIL': email})
    except:
        pass

def handler404(request):
    response = render_to_response('404.html', {}, context_instance=RequestContext(request))
    response.status_code = 404
    return response