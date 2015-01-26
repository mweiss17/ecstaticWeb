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
import logging, json, pprint, datetime, time, hashlib,random,sys

MAILCHIMP_LIST_ID = '4d0c4db173' 
REDIRECT_URL_NAME = '/?email_added=success'

def calculateCurrentTime():
    now = datetime.datetime.utcnow()
    now = time.mktime(now.timetuple()) 
    now = now - 4 * 3600
    return now

def addloginform(context):
    loginform = LoginForm()
    loginform.fields['login'].widget.attrs['class'] = "submit-track user-login"
    loginform.fields['login'].widget.attrs['placeholder'] = "Disco-Name"
    loginform.fields['password'].widget.attrs['class'] = "submit-track user-login"
    loginform.fields['password'].widget.attrs['placeholder'] = "Password"
    context.update({'loginform':loginform})
    return

def index(request):
    upcomingEvents = Events.objects.filter(arrive_start_time__gte=datetime.datetime.now()-datetime.timedelta(seconds=3600*7))
    datetimeNow = datetime.datetime.now()
    TimeZone = datetime.timedelta(seconds=3600*7) #adjustment for EST (4 hrs) + 
                                                  #adjustment for inprogress events (3 hours)
    cities = city.objects.filter()
    previousEvents = Events.objects.filter(arrive_start_time__lte=datetime.datetime.now()-datetime.timedelta(seconds=3600*4))
    upcomingGlobalEvent = globalEvent.objects.filter(arrive_start_time__gte=datetimeNow-TimeZone)
    email_added = ""
    try:
        email_added = request.GET['email_added']
    except Exception, e:
        pass
    try:
        upcomingGlobalEvent = upcomingGlobalEvent[0]
    except Exception, e:
        pass

    template = loader.get_template('index.html')
    context = RequestContext(request, {})
    addloginform(context)
    context.update({'index':True, 'cities':cities, 'upcomingGlobalEvent': upcomingGlobalEvent, 'email_added': email_added, "upcomingEvents":upcomingEvents})

    resp = HttpResponse(template.render(context))
    resp.set_cookie('visited', True)
    return resp


## Want to modify this such that if you get a GET request with a username, you load THAT user, but you 
## don't allow the other user to modify their shiz.
def profile(request):
    context = {}
    addloginform(context)
    cities = city.objects.filter()
    username = request.GET.get('username', '')
    if username != '':
        currentUserProfile = UserProfile.objects.get(user=User.objects.get(username=username))
        context.update({"myprofile":False})
    else:
        currentUserProfile = UserProfile.objects.get(user=request.user)
        context.update({"myprofile":True})

    context.update({'cities':cities, 'currentUserProfile':currentUserProfile})

    pf = photoUploadForm(instance=currentUserProfile.profilePic)
    uf = UpdateProfile(instance=currentUserProfile.user)
    upf = UserProfileForm(instance=currentUserProfile)
    context.update({"uf" : uf, "upf" : upf, "pf":pf})
    return render(request, 'profile.html', context)

def profileupdate(request):
    context = {}
    addloginform(context)
    cities = city.objects.filter()
    pf = photoUploadForm(request.POST, request.FILES, instance=request.user.profile.profilePic)
    uf = UpdateProfile(data=request.POST, instance=request.user)
    upf = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)
    context.update({'uf':uf, 'upf':upf, 'pf':pf})

    if uf.is_valid():
        userObj = uf.save()
        if pf.is_valid():                 
            photoObj = pf.save(commit=False)
            photoObj.user = userObj
            photoObj.save()
        if upf.is_valid():
            userProfileObj = upf.save(commit=False)
            userProfileObj.user = userObj
            userProfileObj.profilePic = photoObj
            userProfileObj.save()
    context.update({"uf" : uf, "upf" : upf, "pf":pf, 'currentUserProfile':UserProfile.objects.get(user=request.user)})
    return render(request, 'profile.html', context)


def about(request):
    context = {}
    addloginform(context)
    cities = city.objects.filter()
    context.update({"cities":cities})
    return render(request, 'about.html', context)

def blog(request):
    cities = city.objects.filter()
    context = {"cities":cities}
    return render(request, 'blog.html', context)

def auth_view(request):
    return

def organize(request):
    cities = city.objects.filter()
    upcomingEvents = Events.objects.filter(arrive_start_time__gte=datetime.datetime.now()-datetime.timedelta(seconds=3600*7))
    context = {}
    addloginform(context)
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
            #print >> sys.stderr, mySubString
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

        context.update({"upcomingEvents":upcomingEvents, "ef":ef, "pf":pf, "cf":cf, "cpf":cpf,'um':um, "cities":cities})
        return render(request, 'organize.html', context)

def event_creation_success(request):
    upcomingEvents = Events.objects.filter(arrive_start_time__gte=datetime.datetime.now()-datetime.timedelta(seconds=3600*7))
    context = {"upcomingEvents":upcomingEvents}
    return render(request, 'event_creation_success.html', context)

def createprofile(request):
    context = {}
    addloginform(context)
    if request.method == 'POST':
        uf = UserCreateForm(request.POST, request.FILES)
        upf = UserProfileForm(request.POST, request.FILES)
        pf = photoUploadForm(request.POST, request.FILES)
        context.update({'uf': uf, 'upf':upf, 'pf':pf})
        profile_CSS(uf, upf)

        if uf.is_valid():
            userObj = uf.save()
            if upf.is_valid():
                print >> sys.stderr, "userprofile is_valid"
                userProfileObj = upf.save(commit=False)
                userProfileObj.user = userObj
                if pf.is_valid():                 
                    photoObj = pf.save(commit=False)
                    photoObj.user = userObj
                    photoObj.save()
                    context.update({'pf':photoObj})
                    userProfileObj.profilePic = photoObj
                email = uf.cleaned_data['email']
                salt = hashlib.sha1(str(random.random())).hexdigest()[:5]            
                userProfileObj.activation_key = hashlib.sha1(salt+email).hexdigest()            
                userProfileObj.key_expires = datetime.datetime.today() + datetime.timedelta(2)
                userProfileObj.save()
                context.update({'upf': userProfileObj})

                # Send email with activation key
                email_subject = 'SDS Account Confirmation'
                email_body = "Hey %s, thanks for signing up. To activate your account, click this link within \
                48hours http://%s/confirm/%s" % (uf.cleaned_data['username'], settings.HOSTNAME, userProfileObj.activation_key)
                send_mail(email_subject, email_body, 'david@silentdiscosquad.com',
                    [email], fail_silently=False)
                if upf.cleaned_data['newsletter']:
                    subscribeToMailchimp(email)
                return render(request, 'register_success.html', context)
        return render(request, 'createprofile.html', context)

    else:
        pf = photoUploadForm()
        uf = UserCreateForm()
        upf = UserProfileForm()
        profile_CSS(uf, upf)
        context.update({"uf" : uf, "upf" : upf, "pf":pf})
        return render(request, 'createprofile.html', context)

def profile_CSS(uf, upf):
    uf.fields['first_name'].widget.attrs['class'] = "formstyle"
    uf.fields['last_name'].widget.attrs['class'] = "formstyle"
    uf.fields['username'].widget.attrs['class'] = "formstyle"
    uf.fields['email'].widget.attrs['class'] = "formstyle"
    uf.fields['password1'].widget.attrs['class'] = "formstyle"
    uf.fields['password2'].widget.attrs['class'] = "formstyle"
    uf.fields['first_name'].widget.attrs['placeholder'] = "First Name"
    uf.fields['last_name'].widget.attrs['placeholder'] = "Last Name"
    uf.fields['username'].widget.attrs['placeholder'] = "Disco Name"
    uf.fields['email'].widget.attrs['placeholder'] = "E-mail"
    uf.fields['password1'].widget.attrs['placeholder'] = "Password"
    uf.fields['password2'].widget.attrs['placeholder'] = "Password (repeat)"
    upf.fields['role'].widget.attrs['class'] = "formstyle"
    upf.fields['dancefloorSuperpower'].widget.attrs['class'] = "formstyle"
    upf.fields['city'].widget.attrs['class'] = "formstyle"
    upf.fields['zipcode'].widget.attrs['class'] = "formstyle"
    upf.fields['role'].widget.attrs['placeholder'] = "Role"
    upf.fields['dancefloorSuperpower'].widget.attrs['placeholder'] = "Dancefloor Superpower"
    upf.fields['city'].widget.attrs['placeholder'] = "What city do you live closest to?"
    upf.fields['zipcode'].widget.attrs['placeholder'] = "zipcode"
    return

def register_confirm(request, activation_key):
    #check if user is already logged in and if he is redirect him to some other url, e.g. home
    if request.user.is_authenticated():
        HttpResponseRedirect('/')

    # check if there is UserProfile which matches the activation key (if not then display 404)
    user_profile = get_object_or_404(UserProfile, activation_key=activation_key)

    #check if the activation key has expired, if it hase then render confirm_expired.html
    if user_profile.key_expires < datetime.datetime.utcnow():
        return render_to_response('user_profile/confirm_expired.html')
    #if the key hasn't expired save user and set him as active and render some template to confirm activation
    user = user_profile.user
    user.is_active = True
    user.save()
    user = authenticate(username=user.username, password=user.password)
    return render_to_response('register_confirm.html')

def register_success(request):
    return render_to_response('register_success.html')
    
def citypage_getthemix(request):
    upcomingEvents = Events.objects.filter(arrive_start_time__gte=datetime.datetime.now()-datetime.timedelta(seconds=3600*7))
    context = {"upcomingEvents":upcomingEvents}
    return render(request, 'citypage_getthemix.html', context)

def future(request):
    context = {}
    addloginform(context)
    cities = city.objects.filter()
    event = Events.objects.get(id=request.GET['id'])
    organizer = UserProfile.objects.get(user=event.organizer)
    if request.method == 'POST':
        form = MusicForm(request.POST, request.FILES)
        uploadedSong = " "
        songName = request.POST['song_name_or_link']

        send_mail('Dancetrack Received', "We got your track! Thanks for your contribution to the Dancemix \nWith Love," +"\nThe SDS Team", 'us@silentdiscosquad.com', [request.POST["email"]], fail_silently=False)            
        send_mail("Received Track from: "+ request.POST['email'], "songname: "+ songName + " intention: "+ request.POST['intention'],'contact@silentdiscosquad.com', ['david@silentdiscosquad.com'], fail_silently=False)       
        if form.is_valid():
            message = "Thanks for submitting your song!"
            form.save()
    else:
        form = MusicForm()
    form.fields['uploadedSong'].widget.attrs['id'] = "fileToUpload"
    form.fields['uploadedSong'].widget.attrs['label'] = "Upload Song"
    form.fields['uploadedSong'].widget.attrs['onchange'] = "fileSelected()"
    form.fields['song_name_or_link'].widget.attrs['class'] = "formstyle"
    form.fields['intention'].widget.attrs['class'] = "formstyle"
    form.fields['email'].widget.attrs['placeholder'] = "Email"
    form.fields['email'].widget.attrs['class'] = "formstyle"
    form.fields['song_name_or_link'].widget.attrs['placeholder'] = "Songname"
    form.fields['intention'].widget.attrs['placeholder'] = "Intention"


    context.update({"form":form, "event":event, "organizer":organizer, "cities":cities})
    return render(request, 'future.html', context)

def citypage_city(request):
    context = {}
    addloginform(context)
    eventCity=str(request.GET['city'])
    upcomingEvents = Events.objects.filter(arrive_start_time__gte=datetime.datetime.now()-datetime.timedelta(seconds=3600*7), eventCity=city.objects.get(cityName=str(request.GET['city'])), active=True)
    community = UserProfile.objects.filter(city=city.objects.get(cityName=str(request.GET['city'])))
    cities = city.objects.filter()


    context.update({"upcomingEvents":upcomingEvents, "community":community, "cities":cities, "eventCity":eventCity})
    return render(request, 'citypage_city.html', context)


def contact(request):
    cities = city.objects.filter()
    context = {"cities":cities}
    addloginform(context)

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
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def mixMailSignup(request):
    #newsletter
    if request.method == 'POST' and 'newsletter' in request.POST and 'email' in request.POST:
        newsletter = request.POST['newsletter']
        email = request.POST['email']
        if newsletter is not None and newsletter != '':
            if email is not None and email != '':
                subscribeToMailchimp(request.POST['email'])
    #Survey     
    if request.method == 'POST' and 'survey' in request.POST and 'email' in request.POST:
        survey = request.POST['survey']
        email = request.POST['email']
        eventPKID = request.POST['id']
        #print >> sys.stderr, request.POST['id']
        if survey is not None and survey != '':
            if email is not None and email != '':
                s = surveySignups(email=email, event=Events.objects.get(pk=eventPKID), mixAccess="download")
                if 'mixAccess' in request.POST:
                    if request.POST['mixAccess'] is not None and request.POST['mixAccess'] != "":
                        s = surveySignups(email=email, event=Events.objects.get(pk=eventPKID), mixAccess=request.POST['mixAccess'])
                s.save()
                text_content = "Hello Dancer,"
                text_content += "\n\nThank you for offering to participate in our survey. Please take 5-10 minutes to fill it out here: https://jfe.qualtrics.com/form/SV_01G8vvjtNXN6Xt3."
                text_content += "There will also be a 2 minute survey sent immediately following the next disco, and a follow-up survey next week. Thanks for your help!"
                text_content += "\n\nMuch love from the SDS Team ~:D"
               # send_mail('Silent Disco Squad Survey', text_content, 'us@silentdiscosquad.com', [request.POST["email"]], fail_silently=False)            


    if request.method == 'POST' and 'download' in request.POST:
        download = request.POST['download']
        if download is not None and download != '':
            return HttpResponseRedirect('https://s3.amazonaws.com/silentdiscosquad/'+download)
    return HttpResponseRedirect('/stream.html/?id='+request.POST['id'])       

def subscribeToMailchimp(email):
    try:
        list = utils.get_connection().get_list_by_id(MAILCHIMP_LIST_ID)
        list.subscribe(email, {'EMAIL': email})
    except:
        pass

def recordEventAttendees(request):
    #check if they have already attended this event
    event = Events.objects.get(id=request.GET['eventID'])
    currentUser = request.user
    
    #if they have attended the event, do nothing
    try:
        attended = EventAttendees.objects.get(event=event, attendee=currentUser)
    
    #if they haven't attended the event (they are not represented in the table) then add them
    except Exception as e:
        print >> sys.stderr, '%s (%s)' % (e.message, type(e))
        ea = EventAttendees(event=event, attendee=currentUser)
        ea.save()

def add_email_to_mailing_list(request):
    if request.POST['email']:
        email_address = request.POST['email']
        list = utils.get_connection().get_list_by_id(MAILCHIMP_LIST_ID)
        list.subscribe(email_address, {'EMAIL': email_address})
        return HttpResponseRedirect('/?email_added=success')
    else:
        return HttpResponseRedirect('/?email_added=failure')

def handler404(request):
    response = render_to_response('404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response
