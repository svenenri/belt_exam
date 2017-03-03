from __future__ import unicode_literals
from django.db import models
from ..login_reg.models import User

# Create your models here.
class TripManager(models.Manager):
	# Validate trip dates
	def checkDates(self, dateFrom, dateTo):
		if dateTo > dateFrom:
			confirm = (True, 'Valid dates')
		else:
			confirm = (False, 'Your Travel To date must be before your Travel From date.')

		return confirm

	def plannerToTrip(self, email, description):
		user = User.objects.get(email= email)
		trip = Trip.objects.get(description= description)
		add = user.planner.set(trip)
		confirm = (True, 'User successfully added to the trip')
		return confirm

	def userToTrip(self, email, description):
		user = User.objects.get(email= email)
		trip = Trip.objects.get(description = description)
		add = trip.traveler.add(user)
		confirm = (True, 'User successfully added to the trip')
		return confirm

	def userToTripById(self, email, id):
		user = User.objects.get(email= email)
		trip = Trip.objects.get(id= id)
		add = trip.traveler.add(user)
		confirm = (True, 'User successfully added to the trip')
		return confirm

class Trip(models.Model):
	destination = models.CharField(max_length=255)
	description = models.TextField()
	planner = models.ManyToManyField(User, default=1, related_name='trip_planner')
	traveler = models.ManyToManyField(User, related_name='travel_user')
	travelToDate = models.DateTimeField(auto_now=False, auto_now_add=False)
	travelFromDate = models.DateTimeField(auto_now=False, auto_now_add=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = TripManager()
