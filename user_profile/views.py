# -*- coding: utf-8 -*-
"""
Copyright © 2017,
Laboratory for Atmospheric Research at Washington State University,
All rights reserved.

"""
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from user_profile.models import AuthToken, AirpactUser
from file_upload.models import Picture
from django.template import RequestContext
from forms import UserCreationForm, EditProfileForm 
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import logout
import json
import random
import string


# View the user profile
@login_required
def user_profile(request):
	if request.user.is_certified is False:
		return render_to_response('not_certified.html')
	if(request.method == 'POST'):
		form = UserProfileForm(request.POST, instance=request.user.profile)

# Login page
def login(request):
	c = {}
	c.update(csrf(request))
	return render_to_response('login.html', c)

# Logout page
@login_required
def logout(request):
	auth.logout(request)
	c = {}
	c.update(csrf(request))
	return render_to_response('login.html', c)

# Authenticate the user
def auth_view(request):
	if(request.method == 'POST'):
		username = request.POST['username']
		password = request.POST['password']


		user = auth.authenticate(username=username, password=password)
		if user is not None:
		   auth.login(request, user)
		   return HttpResponseRedirect("/user/profile/"+ user.username + "/1")
		else:
			return render_to_response('login.html',  {'Errors':"Invalid username or Password"}, context_instance=RequestContext(request) )
	c = {}
	c.update(csrf(request))
	return render_to_response('login.html', c)

# Correct login page
def loggedin(request):
	return render_to_response('loggedin.html')

# Invalid login page
def invalid_login(request):
	return render_to_response('invalid.html')


# Register / Create a new user
def register_user(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/user/')
		else:
			return render_to_response('register.html',  {'form':form}, context_instance=RequestContext(request) )
	form = UserCreationForm()
	return render_to_response('register.html',  {'form':form}, context_instance=RequestContext(request) )

# Registration successful page
def register_success(request): 
	return render_to_response('register_success.html', {'message': "successfull registration! "}, context_instance=RequestContext(request))

# Authentication for the app
@csrf_exempt
def user_app_auth(request):
	if request.method == 'POST':
		userdata = json.loads(request.body)
		print(userdata['username'])
		print(userdata['password'])
		user = auth.authenticate(username=userdata['username'], password=userdata['password'] )
		response_data = {}
		if user is not None and user.is_certified:
			#generate secret key
			secret = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(22))
			secretKey = AuthToken(token = secret)
			secretKey.save()
			response_data['isUser'] = 'true'
			response_data['secretKey'] = secret
		else:
			response_data['isUser'] = 'false'
			response_data['secretKey'] = ''
		print(json.dumps(response_data))
		return HttpResponse(json.dumps(response_data), content_type="application/json")
	else:
		return HttpResponse("HI")

# View the user profile
def view_profile(request, name, page = 1):
	# we need to get the current user info
	# send it to the view...so lets do that I guess
	thisuser = False
	if request.user.username == name:
		thisuser = True
	user = AirpactUser.objects.get(username = name)
	userpictures = Picture.objects.filter(user = user)
	paginator = Paginator(userpictures, 12) #show 12 per page
	try:
		pictures = paginator.page(page)
	except PageNotAnInteger:
		pictures = paginator.page(1)
	except EmptyPage:
		pictures = paginator.page(paginator.num_pages)
	return render_to_response('user_profile.html', {'pictures' : pictures, 'profile_user':user, 'thisuser':thisuser}, context_instance=RequestContext(request))

@login_required
def edit_profile(request):
	if request.user.is_certified is False:
		return render_to_response('not_certified.html')

	userob = AirpactUser.objects.get(username=request.user.username)
	if request.method == 'POST':
		# do stuff to save the new user data
		form = EditProfileForm(request.POST)
		if form.is_valid():
			userob.first_name = form.cleaned_data.get('first_name')
			userob.last_name = form.cleaned_data.get('last_name')
			userob.email = form.cleaned_data.get('email')
			userob.bio = form.cleaned_data.get('bio')
			userob.save()
		#reidrect back to their profile
		return HttpResponseRedirect('/user/profile/'+request.user.username+'/')
	form = EditProfileForm(instance=userob)
	pictures = Picture.objects.filter(user = userob)
	return render_to_response('edit_profile.html', {'user': request.user, 'form':form, 'pictures': pictures}, context_instance=RequestContext(request))

@login_required
def manage_pictures(request):
	userob = AirpactUser.objects.get(username=request.user.username)
	pictures = Picture.objects.filter(user= userob)
	return render_to_response('manage_pictures.html', {'pictures': pictures}, context_instance=RequestContext(request))

@csrf_exempt
@login_required
def admin_page(request):
	if request.user.is_custom_admin is False:
		return HttpResponseRedirect('/')
	if request.user.is_certified is False:
		return render_to_response('not_certified.html')

	nusers = AirpactUser.objects.all()
	if(request.method == 'POST'):
		print(request.POST)
		username = request.POST.get("ourUser",False)
		nuser = AirpactUser.objects.get(username=username)
		the_type = request.POST['the_type']
		
		if(the_type == "certify"):
			nuser.is_certified = True 
			nuser.save()

		if(the_type == "uncertify"):
			nuser.is_certified = False 
			nuser.save()

		if(the_type == "make_admin"):
			nuser.is_custom_admin = True
			nuser.save() 

		if(the_type == "unmake_admin"):
			nuser.is_custom_admin = False
			nuser.save() 

		if(the_type == "delete"):
			nuser.delete()

	return render_to_response('custom_admin_page.html', {'nusers': nusers}, context_instance=RequestContext(request));