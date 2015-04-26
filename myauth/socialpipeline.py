def save_profile(backend, user, response, *args, **kwargs):
    if backend.name == 'facebook':
        profile = user.get_profile()
        print >> sys.stderr, profile.dancefloorSuperpower
        """if profile is None:
            profile = Profile(user_id=user.id)
        profile.gender = response.get('gender')
        profile.link = response.get('link')
        profile.timezone = response.get('timezone')
        profile.save()

		UserProfile = UserProfile
#       userObj = uf.save()
        userProfileObj = upf.save(commit=False)
        userProfileObj.user = user
        photoObj = pf.save(commit=False)
        photoObj.user = userObj
        photoObj.save()
        context.update({'pf':photoObj})
        userProfileObj.profilePic = photoObj
        email = uf.cleaned_data['email']
        salt = hashlib.sha1(str(random.random())).hexdigest()[:5]            
        userProfileObj.save()
        context.update({'upf': userProfileObj})
        if upf.cleaned_data['newsletter']:
            subscribeToMailchimp(email)
        userObj.backend = 'django.contrib.auth.backends.ModelBackend'
        auth.login(request, userObj)
        people_dict = {'$username' : userObj.username, '$create' : datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p"), '$email' : email, 'city' : "none",}
        if userProfileObj.city:
            people_dict['city'] = userProfileObj.city.cityName
        if userObj.first_name:
            people_dict['$first_name'] = userObj.first_name
        if userObj.last_name:
            people_dict['$last_name'] = userObj.last_name
        print >> sys.stderr, userProfileObj.mixpanel_distinct_id
        
        mp.alias(userObj.pk, userProfileObj.mixpanel_distinct_id)
        mp.people_set(userObj.pk, people_dict)
"""