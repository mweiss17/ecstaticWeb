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

#(int) get_distance_in_miles((Point) my_location, (Point) their_location)

#(Void) post_location((Point)my_location, (int) user_id)
def post_location(request):
	#Post the location to the DB
	point = Point(float(request.GET['my_location_lat']), float(request.GET['my_location_lon']))
	user = User.objects.get(id=request.GET['user_id'])
	loc = location.objects.using("ecstatic_geo").create(user=user, point=point)
	loc.save()

	#Delete old location, Cache the new location
	cache.set(user.id,loc.point)
	return HttpResponse("")


#(Point) get_most_recent_location((int)user_id)
def get_most_recent_location(request):
	#user = User.objects.get(id=request.GET['user_id'])
	#loc = location.objects.using("ecstatic_geo").filter(user=user).latest()
	
	#get it from the cache
	if cache.get(request.GET['user_id']) != None:
		return HttpResponse(cache.get(request.GET['user_id']))
	else:
		print >> sys.stderr, "get_most_recent_location cache error, reading from DB"
		user = User.objects.get(id=request.GET['user_id'])
		loc = location.objects.using("ecstatic_geo").filter(user=user).latest()
		return HttpResponse(loc)


#(List<user_id, point>) get_nearest_users((int) number_to_get, (int) user_id)
def get_nearest_users(request):
	context = {}
	user = User.objects.get(id=request.GET['user_id'])
	loc = location.objects.using("ecstatic_geo").filter(user=user).latest()
	points = location.objects.using("ecstatic_geo").filter(
	    point__distance_lte=(loc.point, D(mi=10000))
	).distance(loc.point).order_by('distance')
	context.update({"points":points})
	return HttpResponse(context)


def repopulate_cache():
	returnHttpResponse("oops")