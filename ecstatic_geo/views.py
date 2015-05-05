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

#(Void) post_location((Point)my_location, (int) user_id)
def post_location(request):
	#DATABASE
	point = Point(float(request.GET['my_location_lat']), float(request.GET['my_location_lon']))
	user = User.objects.get(id=request.GET['user_id'])
	loc = location.objects.using("ecstatic_geo").create(user=user, point=point)
	loc.save()

	#CACHE
	cache.set(user.id,loc)
	return HttpResponse("")


#(Point) get_most_recent_location((int)user_id)
def get_most_recent_location(request):

	#CACHE
	if cache.get(request.GET['user_id']) != None:
		user = User.objects.get(id=request.GET['user_id'])
		loc = cache.get(request.GET['user_id'])
		return HttpResponse(json.dumps({"user":user.username, "point_lat":loc.point.x, "point_lon":loc.point.y, "timestamp":loc.timestamp.isoformat()}))

	#DATABASE
	else:
		print >> sys.stderr, "get_most_recent_location cache error, reading from DB"
		user = User.objects.get(id=request.GET['user_id'])
		loc = location.objects.using("ecstatic_geo").filter(user=user).latest()
		return HttpResponse(loc)


#(List<user_id, point>) get_nearest_users((int) number_to_get, (int) user_id)

def get_nearest_users(request):
	#set some variables
	user = User.objects.get(id=request.GET['user_id'])
 	my_location = location.objects.using("ecstatic_geo").filter(user=user).latest()
 	my_point = my_location.point
	number_of_users = request.GET['number_of_users']
	radius_in_miles = 10000
	current_locations = []
	valid_locations = []
	users = User.objects.all()

	#CACHE:
	#get all current locations
	"""for user in users:
		try:
			if cache.get(user.id) is not None:
				current_locations.append(cache.get(user.id))
		except Exception as e:
		    print >> sys.stderr, '%s (%s)' % (e.message, type(e))
	print >> sys.stderr, current_locations

	#check if current_location is near my_point
	for l in current_locations:
		if my_point.distance(l.point) < radius_in_miles:
			valid_locations.append(l)

	if valid_locations:
		return HttpResponse([valid_locations])
"""
	#DATABASE: Database gets tried if there are no valid locations 
	#get all current locations
	for user in users:
		try:
			current_locations.append(location.objects.using("ecstatic_geo").filter(user=user).latest())
		except Exception as e:
		    print >> sys.stderr, '%s (%s)' % (e.message, type(e))
	
	#check if current_location is near my_point
	for l in current_locations:
		if my_point.distance(l.point) < radius_in_miles:
			valid_locations.append(l)
	return HttpResponse(valid_locations)

#(int) get_distance_in_miles((Point) my_location, (Point) their_location)

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