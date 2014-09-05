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
from django.contrib import auth
from django.core.context_processors import csrf
from mailchimp import utils
from django.contrib.auth.forms import *
import logging, json, pprint, datetime, time, hashlib,random

def calculateCurrentTime():
    now = datetime.datetime.utcnow()
    now = time.mktime(now.timetuple()) 
    now = now - 4 * 3600
    return now

def index(request):
    datetimeNow = datetime.datetime.now()
    TimeZone = datetime.timedelta(seconds=3600*7) #adjustment for EST (4 hrs) + 
                                                  #adjustment for inprogress events (3 hours)
    #upcomingEvents = Events.objects.filter(arrive_start_time__gte=datetimeNow-TimeZone)
    #tempUpcomingEventsCities = []
    #for e in upcomingEvents:
    #    tempUpcomingEventsCities.append(e.eventCity.cityName)
    #upcomingEventsCities = set(tempUpcomingEventsCities)
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

    authform = AuthenticationForm(request)
    authform.fields['username'].widget.attrs['class'] = "submit-track user-login"
    authform.fields['username'].widget.attrs['placeholder'] = "Disco-Name"
    authform.fields['password'].widget.attrs['class'] = "submit-track user-login"
    authform.fields['password'].widget.attrs['placeholder'] = "Password"

    context = RequestContext(request, {'index':True, 'cities':cities, 'upcomingGlobalEvent': upcomingGlobalEvent, 'email_added': email_added, "authform":authform})

    resp = HttpResponse(template.render(context))
    resp.set_cookie('visited', True)
    return resp



def about(request):
    context = {}
    return render(request, 'about.html', context)

def blog(request):
    context = {}
    return render(request, 'blog.html', context)

def organize(request):
    upcomingEvents = Events.objects.filter(arrive_start_time__gte=datetime.datetime.now()-datetime.timedelta(seconds=3600*7))
    authform = AuthenticationForm(request)
    authform.fields['username'].widget.attrs['class'] = "submit-track user-login"
    authform.fields['username'].widget.attrs['placeholder'] = "Disco-Name"
    authform.fields['password'].widget.attrs['class'] = "submit-track user-login"
    authform.fields['password'].widget.attrs['placeholder'] = "Password"

    context = {}
    if request.method == 'POST':
        ef = eventForm(request.POST)
        pf = photoUploadForm(request.POST, request.FILES)
        cf = cityForm(request.POST)
        cpf = photoUploadForm(request.POST, request.FILES)
        context['ef'] = ef
        context['pf'] = pf
        context['cf'] = cf
        context['cpf'] = cpf
        if pf.is_valid():                 
            photoObj = pf.save(commit=False)
            photoObj.user = request.user
            photoObj.save()
        if ef.is_valid():
            eventObject = ef.save(commit=False)
            eventObject.eventPic = photoObj
            eventObject.organizer = request.user
            if cf.is_valid() and cpf.is_valid():
                cityPhotoObject = cpf.save(commit=False)
                cityPhotoObject.user = request.user
                cityPhotoObject.save()
                cityObject = cf.save(commit=False)
                cityObject.cityImage = cityPhotoObject
                cityObject.save()
                eventObject.city = cityObject
            eventObject.save()
            return render(request, 'event_creation_success.html', context)
        else:
            return render(request, 'fuck.html', context)
    else:
        ef = eventForm()
        pf = photoUploadForm()
        cf = cityForm()
        cpf = photoUploadForm()

        ef.fields['title'].widget.attrs['class'] = "register-field"
        ef.fields['eventCity'].widget.attrs['class'] = "register-field"
        ef.fields['location'].widget.attrs['class'] = "register-field"
        ef.fields['google_map_link'].widget.attrs['class'] = "register-center-field"

        ef.fields['title'].widget.attrs['placeholder'] = "Title"
        ef.fields['arrive_start_time'].widget.attrs['placeholder'] = "When should people arrive?"
        ef.fields['music_start_time'].widget.attrs['placeholder'] = "When does the mix begin?"
        ef.fields['eventCity'].widget.attrs['placeholder'] = "City"
        ef.fields['location'].widget.attrs['placeholder'] = "Specific Location"
        ef.fields['google_map_link'].widget.attrs['placeholder'] = "Google Maps Link"

        ef.fields['arrive_start_time'].widget.attrs['data-format'] = "MM/dd/yyyy hh:mm"
        ef.fields['music_start_time'].widget.attrs['data-format'] = "MM/dd/yyyy hh:mm"

        cf.fields['cityName'].widget.attrs['class'] = 'register-field'
        cf.fields['cityName'].widget.attrs['placeholder'] = 'My City\'s Name'

        context = {"upcomingEvents":upcomingEvents, "ef":ef, "pf":pf, "cf":cf, "cpf":cpf, "authform":authform}
        return render(request, 'organize.html', context)

def event_creation_success(request):
    upcomingEvents = Events.objects.filter(arrive_start_time__gte=datetime.datetime.now()-datetime.timedelta(seconds=3600*7))
    context = {"upcomingEvents":upcomingEvents}
    return render(request, 'event_creation_success.html', context)

def profile(request):
    authform = AuthenticationForm(request)
    authform.fields['username'].widget.attrs['class'] = "submit-track user-login"
    authform.fields['username'].widget.attrs['placeholder'] = "Disco-Name"
    authform.fields['password'].widget.attrs['class'] = "submit-track user-login"
    authform.fields['password'].widget.attrs['placeholder'] = "Password"
    context = {}
    if request.method == 'POST':
        uf = UserCreateForm(request.POST, request.FILES)
        upf = UserProfileForm(request.POST, request.FILES)
        pf = photoUploadForm(request.POST, request.FILES)
        context['uf'] = uf
        context['upf'] = upf
        context['pf'] = pf
        profile_CSS(uf, upf)

        if uf.is_valid():
            userObj = uf.save()
            if pf.is_valid():                 
                photoObj = pf.save(commit=False)
                photoObj.user = userObj
                photoObj.save()
                context['pf'] = photoObj
            if upf.is_valid():
                userProfileObj = upf.save(commit=False)
                userProfileObj.user = userObj
                userProfileObj.profilePic = photoObj
                email = uf.cleaned_data['email']
                salt = hashlib.sha1(str(random.random())).hexdigest()[:5]            
                userProfileObj.activation_key = hashlib.sha1(salt+email).hexdigest()            
                userProfileObj.key_expires = datetime.datetime.today() + datetime.timedelta(2)
                userProfileObj.save()
                context['upf'] = userProfileObj

                # Send email with activation key
                email_subject = 'SDS Account Confirmation'
                email_body = "Hey %s, thanks for signing up. To activate your account, click this link within \
                48hours http://54.186.184.253/confirm/%s" % (uf.cleaned_data['username'], userProfileObj.activation_key)
                send_mail(email_subject, email_body, 'david@silentdiscosquad.com',
                    [email], fail_silently=False)
                return render(request, 'register_success.html', context)
        return render(request, 'profile.html', context)

    else:
        pf = photoUploadForm()
        uf = UserCreateForm()
        upf = UserProfileForm()
        profile_CSS(uf, upf)
        context = {"uf" : uf, "upf" : upf, "pf":pf}
        return render(request, 'profile.html', context)

def profile_CSS(uf, upf):
    uf.fields['first_name'].widget.attrs['class'] = "register-field"
    uf.fields['last_name'].widget.attrs['class'] = "register-center-field"
    uf.fields['username'].widget.attrs['class'] = "register-field"
    uf.fields['email'].widget.attrs['class'] = "register-field"
    uf.fields['password1'].widget.attrs['class'] = "register-field"
    uf.fields['password2'].widget.attrs['class'] = "register-center-field"
    uf.fields['first_name'].widget.attrs['placeholder'] = "First Name"
    uf.fields['last_name'].widget.attrs['placeholder'] = "Last Name"
    uf.fields['username'].widget.attrs['placeholder'] = "Disco Name"
    uf.fields['email'].widget.attrs['placeholder'] = "E-mail"
    uf.fields['password1'].widget.attrs['placeholder'] = "Password"
    uf.fields['password2'].widget.attrs['placeholder'] = "Password (repeat)"
    upf.fields['role'].widget.attrs['class'] = "register-field"
    upf.fields['dancefloorSuperpower'].widget.attrs['class'] = "register-field"
    upf.fields['city'].widget.attrs['class'] = "register-field"
    upf.fields['zipcode'].widget.attrs['class'] = "register-field"
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
    if user_profile.key_expires < timezone.now():
        return render_to_response('user_profile/confirm_expired.html')
    #if the key hasn't expired save user and set him as active and render some template to confirm activation
    user = user_profile.user
    user.is_active = True
    user.save()
    user = authenticate(username=user.username, password=user.password)
    return render_to_response('register_confirm.html')

def register_success(request):
    render_to_response('register_success.html')
    
def citypage_getthemix(request):
    upcomingEvents = Events.objects.filter(arrive_start_time__gte=datetime.datetime.now()-datetime.timedelta(seconds=3600*7))
    context = {"upcomingEvents":upcomingEvents}
    return render(request, 'citypage_getthemix.html', context)

def future(request):
    event = Events.objects.get(id=request.GET['id'])
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

    authform = AuthenticationForm(request)
    authform.fields['username'].widget.attrs['class'] = "submit-track user-login"
    authform.fields['username'].widget.attrs['placeholder'] = "Disco-Name"
    authform.fields['password'].widget.attrs['class'] = "submit-track user-login"
    authform.fields['password'].widget.attrs['placeholder'] = "Password"

    context = {"form":form, "authform":authform, "event":event}
    return render(request, 'future.html', context)

def citypage_city(request):
    eventCity=str(request.GET['city'])
    upcomingEvents = Events.objects.filter(arrive_start_time__gte=datetime.datetime.now()-datetime.timedelta(seconds=3600*7), eventCity=city.objects.get(cityName=str(request.GET['city'])))
    community = UserProfile.objects.filter(city=city.objects.get(cityName=str(request.GET['city'])))
    cities = city.objects.filter()

    authform = AuthenticationForm(request)
    authform.fields['username'].widget.attrs['class'] = "submit-track user-login"
    authform.fields['username'].widget.attrs['placeholder'] = "Disco-Name"
    authform.fields['password'].widget.attrs['class'] = "submit-track user-login"
    authform.fields['password'].widget.attrs['placeholder'] = "Password"

    context = {"upcomingEvents":upcomingEvents, "authform":authform, "community":community, "cities":cities, "eventCity":eventCity}
    return render(request, 'citypage_city.html', context)


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
    
def auth_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = auth.authenticate(username=username, password=password)
    context = {}
    if user is not None:
        auth.login(request, user)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'), context)
    else:
        context = {'invalid_login': True}
        return HttpResponseRedirect(user, context)
    
def logout(request):
    auth.logout(request)
    context = {}
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
        eventPKID = request.POST['id']
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
                send_mail('Silent Disco Squad Survey', text_content, 'us@silentdiscosquad.com', [request.POST["email"]], fail_silently=False)            


    if request.method == 'POST' and 'download' in request.POST:
        download = request.POST['download']
        if download is not None and download != '':
            return HttpResponseRedirect('https://s3.amazonaws.com/silentdiscosquad/'+download)
    return HttpResponseRedirect('/stream.html/?id='+request.POST['id'])       

def add_email_to_mailing_list(request):
    if request.POST['email']:
        email_address = request.POST['email']
        list = utils.get_connection().get_list_by_id(MAILCHIMP_LIST_ID)
        list.subscribe(email_address, {'EMAIL': email_address})
        return HttpResponseRedirect('/?email_added=success')
    else:
        return HttpResponseRedirect('/?email_added=failure')

