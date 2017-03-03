from django.shortcuts import render, redirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib import messages
from .models import Trip
from ..login_reg.models import User


# Create your views here.
def travel(request):
	userInfo = User.objects.getUserByEmail(request.session['email'])
	tripInfo = Trip.objects.filter(traveler__email = request.session['email']).order_by('travelFromDate')
	otherTrips = Trip.objects.exclude(traveler__email = request.session['email']).order_by('travelFromDate')
	context = {
		'userInfo': userInfo,
		'tripInfo': tripInfo,
		'otherTrips': otherTrips
	}
	return render(request, 'travel/travel.html', context)

def add(request):
	return render(request, 'travel/add.html')

def process(request):
	# Get information for trip to be added
	destination = request.POST['destination']
	description = request.POST['description']
	dateFrom = request.POST['dateFrom']
	dateTo = request.POST['dateTo']

	# Email for performing get to add user to the trip
	email = request.session['email']

	# Validate that dateFrom is not > dateTo
	validDates = Trip.objects.checkDates(dateFrom, dateTo)
	if validDates[0] == False:
		messages.error(request, validDates[1])
		return redirect(reverse('travel:add'))
	else:
		# Create trip in Db
		addTrip = Trip.objects.create(destination=destination, description=description, travelToDate=dateTo, travelFromDate=dateFrom)

		# Add trip planner
		# addPlanner = Trip.objects.plannerToTrip(email, description)

		# Add user to the newly created trip
		addUser = Trip.objects.userToTrip(email, description)

		return redirect(reverse('travel:travel'))

def join(request, id):
	# Email for performing get to add user to the trip
	email = request.session['email']

	# Add user to the selected trip
	addUser = Trip.objects.userToTripById(email, id)
	if addUser[0] == True:
		messages.success(request, addUser[1])
	else:
		messages.error(request, 'An error occured while joining user to the selected trip.')
	return redirect(reverse('travel:travel'))

def destination(request, id):
	trip = Trip.objects.filter(id = id)
	travelers = User.objects.filter(travel_user__id = id)
	context = {
		'trip': trip,
		'travelers': travelers,
	}
	return render(request, 'travel/destination.html', context)
