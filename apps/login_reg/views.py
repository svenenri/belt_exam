from django.shortcuts import render, redirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib import messages
from .models import User

# Project Views
def main(request):
	return render(request, 'login_reg/main.html')

def process(request):
	if request.method == 'POST':
		if request.POST['submit'] == 'Register':
			# Get registration information
			name = request.POST['name']
			alias = request.POST['alias']
			email = request.POST['email']

			validateInfo = {
				'name': name,
				'alias': alias,
				'email': email,
			}

			# Checking validity of the user-entered info.
			checkInfo = User.objects.validate(validateInfo)
			if checkInfo:
				for idx in range(len(checkInfo)):
					messages.error(request, checkInfo[idx])
				return redirect(reverse('login_reg:main'))

			#Verify that user is not already in the Db
			userCheck = User.objects.getUserByEmail(email)
			if userCheck:
				messages.error(request, 'This email is already in the database. Please register with a different email.')
				return redirect(reverse('login_reg:main'))
			else:
				# Check the length of the entered password and that password and confirm password match. If both are true then secure the password using bcrypt.
				pwCheck = User.objects.pwSecure(request.POST['password'], request.POST['pwConfirm'])
				if pwCheck[0] == True:
					# Adding new user to Db
					userAdd = User.objects.addUser(validateInfo, pwCheck[1])

					# Get user info and redirect to main travel page
					newUserGet = User.objects.getUserByEmail(email)
					request.session['email'] = email
					messages.success(request, 'Successfully logged in!')
					return redirect(reverse('travel:travel'))
				else:
					for idx in range(len(pwCheck[1])):
						messages.error(request, pwCheck[1][idx])
					return redirect(reverse('login_reg:main'))

		elif request.POST['submit'] == 'Login':
			# Get entered login information
			email = request.POST['email']
			password = request.POST['password']

			# Query Db for user based on entered email
			findUser = User.objects.getUserByEmail(email)

			# If verify user exists in Db. If yes, send to travel page. if no tell user to register
			if findUser:
				for user in findUser:
					pwUser = user.password
					id = user.id

				# Verify that pw matches what's in the Db
				confirmPW = User.objects.pwVerifyLogin(password, pwUser)

				if confirmPW[0] == True:
					request.session['email'] = email
					messages.success(request, confirmPW[1])
					return redirect(reverse('travel:travel'))
				else:
					messages.error(request, confirmPW[1])
					return redirect(reverse('login_reg:main'))
			else:
				messages.error(request, 'User not found. Please Register above.')
				return redirect(reverse('login_reg:main'))

# def success(request, id):
# 	userInfo = User.objects.getUserByEmail(request.session['email'])
# 	for info in userInfo:
# 		id = info.id
# 	context = {
# 		'userInfo': userInfo
# 	}
# 	return render(request, 'login_reg/success.html', context)

def logout(request):
	for stuff in request.session:
		del stuff
	messages.success(request, 'You have successfully logged out.')
	return redirect(reverse('login_reg:main'))
