from __future__ import unicode_literals
from django.db import models
import bcrypt
import re

# Project Models and logic
class ManageUser(models.Manager):
	# Validate first, last, and email
	def validate(self, info):
		# Regex validators
		emailValidate = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
		nameValidate = re.compile(r'^[A-Za-z]+ [A-Za-z]+$')
		aliasValidate = re.compile(r'^[A-Za-z]+$')

		# Dictionary of potential error messages
		errorMessages = {
			'name': 'Name is not valid. Name must be at least 2 characters and not contain any numbers or special characters.',
			'alias': 'Alias is not valid. Alias must be at least 2 characters and not contain any numbers or special characters.',
			'email': 'Email is not valid.'
		}

		# This list will hold any errors that need to be thrown in messages.
		returnErrors = []

		# Validate the first name that was entered.
		if len(info['name']) < 2 or not nameValidate.match(info['name']):
			returnErrors.append(errorMessages['name'])

		# Validate the alias that was entered.
		if len(info['alias']) < 2 or not aliasValidate.match(info['alias']):
			returnErrors.append(errorMessages['alias'])

		# Validate the email that was entered.
		if len(info['email']) < 1 or not emailValidate.match(info['email']):
			returnErrors.append(errorMessages['email'])

		return returnErrors

	# Verify password length
	def pwLength(self, password):
		if len(password) < 8:
			errorMsg = 'Your password must be at least 8 characters.'
			match = (False, errorMsg)
			return match
		else:
			match = (True, 'Length confirmed.')
			return match

	# Verify pw vs pwConfirm
	def pwVerify(self, password, pwConfirm):
		if password != pwConfirm:
			errorMsg = 'Password and Confirm Password must match.'
			match = (False, errorMsg)
			return match
		else:
			match = (True, 'Password and Confirm Password match.')
			return match

	# securePW
	def pwSecure(self, password, pwConrirm):
		length = self.pwLength(password)
		isMatch = self.pwVerify(password, pwConrirm)

		if length[0] == True and isMatch[0] == True:
			# Encrypt PW using bcrypt and check validity
			password = password.encode()
			pwHashSalt = bcrypt.hashpw(password, bcrypt.gensalt())
			isSecure = (True, pwHashSalt)
			return isSecure
		else:
			errorMsgs = [length[1], isMatch[1]]
			isSecure = (False, errorMsgs)
			return isSecure

	# Verify PW on Login
	def pwVerifyLogin(self, password, pwConfirm):
		password = password.encode()
		pwConfirm = pwConfirm.encode()

		if bcrypt.hashpw(password, pwConfirm) == pwConfirm:
			verifyMsg = 'Successfully logged in!'
			verified = (True, verifyMsg)
			return verified
		else:
			verifyMsg = 'Invalid username and/or password.'
			verified = (False, verifyMsg)
			return verified

	# Find user by email
	def getUserByEmail(self, email):
		user = self.filter(email = email)
		return user

	# Find user by id
	def getUserByID(self, id):
		user = self.filter(id = id)
		return user

	# Get all users
	def getAllUsers(self):
		users = self.all()
		return users

	# Add a new user
	def addUser(self, info, password):
		self.create(name = info['name'], alias = info['alias'], email = info['email'], password = password)

		confirmMsg = 'New user has been successfully added.'
		# Tuple with bool added for use with functionality to be added later where the length of entries passed in by user is checked for valid length.
		confirm = (True, confirmMsg)
		return confirm

class User(models.Model):
	name = models.CharField(max_length=255)
	alias = models.CharField(max_length=50)
	email = models.CharField(max_length=100)
	password = models.CharField(max_length=500)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = ManageUser()

	def __str__(self):
		print self.name
