from django.http import HttpResponse
from django.shortcuts import *
from sds.models import Photos, Music, Events, globalEvent, surveySignups
from sds.forms import surveySignupsForm
from django.template import RequestContext, loader
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.generic import FormView
from django.core.urlresolvers import reverse
from django.forms import ModelForm
from django.forms.models import modelform_factory
from sds.forms import MusicForm
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.contrib import auth
from django.core.context_processors import csrf
from mailchimp import utils
import logging, json, pprint, datetime, time

def calculateCurrentTime():
    now = datetime.datetime.utcnow()
    now = time.mktime(now.timetuple()) 
    now = now - 4 * 3600
    return now

def index(request):
    datetimeNow = datetime.datetime.now()
    TimeZone = datetime.timedelta(seconds=3600*7) #adjustment for EST (4 hrs) + 
                                                  #adjustment for inprogress events (3 hours)
    upcomingEvents = Events.objects.filter(arrive_start_time__gte=datetimeNow-TimeZone)
    previousEvents = Events.objects.filter(arrive_start_time__lte=datetime.datetime.now()-datetime.timedelta(seconds=3600*4))
    upcomingGlobalEvent = globalEvent.objects.filter(arrive_start_time__gte=datetimeNow-TimeZone)
    invalid_login = False
    email_added = ""
    try:
        email_added = request.GET['email_added']
    except Exception, e:
        pass
    try:
        upcomingGlobalEvent = upcomingGlobalEvent[0]
    except Exception, e:
        pass



    future = 'False'
    etaList = []
    upcomingEventsList = []
    template = loader.get_template('index.html')
    for event in upcomingEvents:
        eventstart = event.music_start_time
        eventstart = time.mktime(eventstart.timetuple())
        etaList.append(eventstart-calculateCurrentTime())
        upcomingEventsList.append(event.id)


    showLightbox = True
    if 'visited' in request.COOKIES:
        showLightbox = False


    context = RequestContext(request, {
        'future': future, 'upcomingEvents': upcomingEvents, 'etaList': etaList, 'upcomingEventsList': upcomingEventsList, 'previousEvents': previousEvents, 'invalid_login': invalid_login, 'showLightbox': showLightbox, 'upcomingGlobalEvent': upcomingGlobalEvent, 'email_added': email_added
    })

    resp = HttpResponse(template.render(context))
    resp.set_cookie('visited', True)
    return resp

def future(request):
    MusicForm = modelform_factory(Music, fields=("email", "song_name_or_link", "intention", "uploadedSong"))
    message = ""
    if request.method == 'POST':
        form = MusicForm(request.POST, request.FILES)
        uploadedSong = " "
        songName = request.POST['song_name_or_link']

        send_mail('Dancetrack Received', "We got your track! Thanks for your contribution to the Dancemix!" + "\nLast Favour! From now until October we have a quick Survey (https://jfe.qualtrics.com/form/SV_01G8vvjtNXN6Xt3) that helps us better understand the effects of participating in Silent Disco Squad - Please take 5-10 Mins and fill it out! " + "\nWith Love," +"\nThe SDS Team", 'us@silentdiscosquad.com', [request.POST["email"]], fail_silently=False)            
        send_mail("Song Submission from: "+ request.POST['email'], "songname: "+ songName + " intention: "+ request.POST['intention'],'contact@silentdiscosquad.com', ['david@silentdiscosquad.com'], fail_silently=False)       
        if form.is_valid():
            message = "Thanks for submitting your song!"
            form.save()
    else:
        form = MusicForm()
    
    event = Events.objects.filter(id=request.GET['id'])
    event = event[0]
    eventstart = event.music_start_time
    eventstart = time.mktime(eventstart.timetuple())
    upcomingEventsList = []
    upcomingEventsList.append(event.id)

    etaList = []
    etaList.append(eventstart - calculateCurrentTime())

    context = {'success': message, 'form': form, 'event': event, 'globalEvent': event.globalEvent, 'etaList': etaList, 'upcomingEventsList': upcomingEventsList}
    return render_to_response('index_future.html', context, context_instance=RequestContext(request))

def contact(request):
    context = {}
    if request.method == 'POST':
            send_mail("From: "+request.POST['email']+" "+request.POST['subject'], request.POST['message'], "contact@silentdiscosquad.com" , ['martin@silentdiscosquad.com', 'david@silentdiscosquad.com'])
    return render(request, 'contact.html', context)

def mission(request):
    context = {}
    return render(request, 'mission.html', context)

def become(request):
    context = {}
    return render(request, 'index_join_become.html', context)

def form(request):
    template = loader.get_template('form.html')
    context = {}
    return render(request, 'form.html', context)

def userauth(request):
    context={'user' : request.user, 'pw' : request.user.is_authenticated()}
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
    event = Events.objects.filter(id=request.GET['id'])
    event = event[0]

    eventstart = event.music_start_time
    eventstart = time.mktime(eventstart.timetuple())
    eta = eventstart - calculateCurrentTime()
    eta = -eta
    context = {'event': event, 'eta': eta}
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
    datetimeNow = datetime.datetime.now()
    TimeZone = datetime.timedelta(seconds=3600*7) #adjustment for EST (4 hrs) + 
                                                  #adjustment for inprogress events (3 hours)
    upcomingEvents = Events.objects.filter(arrive_start_time__gte=datetimeNow-TimeZone)
    previousEvents = Events.objects.filter(arrive_start_time__lte=datetime.datetime.now()-datetime.timedelta(seconds=3600*4))
    upcomingGlobalEvent = globalEvent.objects.filter(arrive_start_time__gte=datetimeNow-TimeZone)

    future = 'False'
    etaList = []
    upcomingEventsList = []

    some_data_to_dump = []
    for event in upcomingEvents:
        eventstart = event.music_start_time
        eventstart = time.mktime(eventstart.timetuple())
        etaList.append(eventstart-calculateCurrentTime())
        upcomingEventsList.append(event.id)
        some_data_to_dump.append({'id': event.id, 'title': event.title, 'start':eventstart, 'city': event.city, 'location':event.location, 'map':event.google_map_link, 'fbevent':event.fbEvent, 'latitude':event.latitude, 'longitude':event.longitude, 'songTitle':event.eventMix.uploadedSong.url})
        #logger = logging.getLogger(__name__)
        #logger.debug(eventstart)

    data = json.dumps(some_data_to_dump)

    context = RequestContext(request, {
        'future': future, 'upcomingEvents': upcomingEvents, 'etaList': etaList, 'upcomingEventsList': upcomingEventsList, 'previousEvents': previousEvents
    })
    return HttpResponse(data, mimetype='application/json')

def login(request):
    c = {}
    c.update(csrf(request))    
    return render_to_response('login.html', c)
    
def auth_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    context = {}
    if user is not None:
        auth.login(request, user)
        return HttpResponseRedirect('/', context)
    else:
        context = {'invalid_login': True}
        return HttpResponseRedirect('/?invalid_login=true', context)
    
def loggedin(request):
    context = {'full_name': request.user.username}
    return render(request, 'index', context)

def invalid_login(request):
    return render_to_response('invalid_login.html')

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')


MAILCHIMP_LIST_ID = '4d0c4db173' # DRY :)
REDIRECT_URL_NAME = '/?email_added=success'

def mixMailSignup(request):
    #newsletter
    if request.method == 'POST' and 'newsletter' in request.POST and 'email' in request.POST:
        newsletter = request.POST['newsletter']
        email = request.POST['email']
        if newsletter is not None and newsletter != '':
            if email is not None and email != '':
                email_address = request.POST['email']
                list = utils.get_connection().get_list_by_id(MAILCHIMP_LIST_ID)
                list.subscribe(email_address, {'EMAIL': email_address})
    #Survey     
    if request.method == 'POST' and 'survey' in request.POST and 'email' in request.POST:
        survey = request.POST['survey']
        email = request.POST['email']
        if survey is not None and survey != '':
            if email is not None and email != '':
                s = surveySignups(email=email, event=Events.objects.get(pk=request.POST['id']))
                s.save()
                text_content = "Hello Dancer,"
                text_content += "\n\nThank you for offering to participate in our survey. Please take 5-10 minutes to fill it out here: https://jfe.qualtrics.com/form/SV_01G8vvjtNXN6Xt3."
                text_content += "There will also be a 2 minute survey sent immediately following the next disco, and a follow-up survey next week. Thanks for your help!"
                text_content += "\n\nMuch love from the SDS Team ~:D"
                send_mail('Silent Disco Squad Survey', text_content, 'us@silentdiscosquad.com', [request.POST["email"]], fail_silently=False)            


    if request.method == 'POST' and 'download' in request.POST:
        download = request.POST['download']
        if download is not None and download != '':
            return HttpResponseRedirect('https://s3.amazonaws.com/silentdiscosquad/'+download)
    return HttpResponseRedirect('/stream.html/?id='+request.POST['id'])   

    #Neither Checked 



def add_email_to_mailing_list(request):
    if request.POST['email']:
        email_address = request.POST['email']
        list = utils.get_connection().get_list_by_id(MAILCHIMP_LIST_ID)
        list.subscribe(email_address, {'EMAIL': email_address})
        return HttpResponseRedirect('/?email_added=success')
    else:
        return HttpResponseRedirect('/?email_added=failure')

