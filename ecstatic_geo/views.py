from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.gis.geos import Point
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D
from django.core.cache import cache
from models import *
from myauth.models import * 
from django.conf import settings
from sds.settings import *
import json
from math import radians, cos, sin, asin, sqrt


#(Void) post_location((Point)my_location, (string) username)
def post_location(request):
	#DATABASE
	print >> sys.stderr, request.POST['my_location_lat']
	point = Point(float(request.POST['my_location_lat']), float(request.POST['my_location_lon']))
	user = User.objects.get(username=request.POST['username'])
	loc = location.objects.using("ecstatic_geo").create(user=user, point=point)
	loc.save()

	#CACHE
	cache.set(user.username, loc, timeout=0)
	return HttpResponse("location_received")


#(Point) get_most_recent_location((string)username)
def get_most_recent_location(request):

	#CACHE
	if cache.get(request.GET['username']) != None:
		user = User.objects.get(username=request.GET['username'])
		loc = cache.get(request.GET['username'])
		return HttpResponse(json.dumps({"username":user.username, "point_lat":loc.point.x, "point_lon":loc.point.y, "timestamp":loc.timestamp.isoformat()}))

	#DATABASE
	else:
		print >> sys.stderr, "get_most_recent_location cache error, reading from DB"
		user = User.objects.get(username=request.GET['username'])
		loc = location.objects.using("ecstatic_geo").filter(user=user).latest()
		return HttpResponse(loc)


#(List<username, point>) get_nearest_users((int) number_to_get, (int) username)

def get_nearest_users(request):
	#set some variables
	user = User.objects.get(username=request.GET['username'])
 	my_location = location.objects.using("ecstatic_geo").filter(user=user).latest()
 	my_point = my_location.point
	radius_in_miles = 10000
	current_locations = []
	valid_locations = []
	users = User.objects.all()

	for user in users:
		try:
			current_locations.append(location.objects.using("ecstatic_geo").filter(user=user).latest())
		except Exception as e:
			pass

	#check if current_location is near my_point
	for l in current_locations:
		d = haversine(my_point.y, my_point.x, l.point.y, l.point.x)
		room_number = cache.get(l.user.username+":room")
		j = json.dumps({"distance":d, "user":l.user.username, "room_number":room_number})
		valid_locations.append(j)
	str1 = ', '.join(valid_locations)
	str2 = '{"locations":['+ str1 + ']}'
	
	return HttpResponse(str2)



#(int) get_distance_in_kilometers((Point) my_location, (Point) their_location)
def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    km = 6367 * c
    return km



#For each user, put that users most recent location into the cache
def repopulate_cache(): 
	users = User.objects.all()
	most_recent_location = []
	for user in users:
		try:
			cache.set(user.id, location.objects.using("ecstatic_geo").filter(user=user).latest())
		except Exception as e:
		    print >> sys.stderr, '%s (%s)' % (e.message, type(e))
	return HttpResponse("")