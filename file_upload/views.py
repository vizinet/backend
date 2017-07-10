# -*- coding: utf-8 -*-
"""
Copyright © 2017,
Laboratory for Atmospheric Research at Washington State University,
All rights reserved.

"""
# Django Libraries
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.files.base import ContentFile
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

# Custom Django
from file_upload.models import Picture, Tag, AlgorithmOne, AlgorithmTwo
from user_profile.models import AuthToken, AirpactUser
from user_profile.views import edit_profile
from file_upload.forms import picture_upload_form, algorithm_one_form, algorithm_two_form
from convos.forms import comment_form

# Other
from base64 import b64decode
from time import time
import datetime
import json

# TODO: 
# Create time taken field in picture table
#

# Are we debuggin?
def debugging():
	return True

# Returns list of algorithm objects given its picture *Note the list should contain 
# Only one value
def retreive_algorithm_object(Picture):
	return {
	"AlgorithmOne" : AlgorithmOne.objects.filter(picture = Picture),
	"AlgorithmTwo" : AlgorithmTwo.objects.filter(picture = Picture)
	}[Picture.algorithmType]

# Retreives am algorithm form given a picture
def retreive_algorithm_form(Picture, postData = None, fileData = None):
	if postData is None:
		return {
		"AlgorithmOne" : algorithm_one_form(),
		"AlgorithmTwo" : algorithm_two_form()
		}[Picture.algorithmType]
	else:
		return {
		"AlgorithmOne" : algorithm_one_form(postData),
		"AlgorithmTwo" : algorithm_two_form(postData, fileData)
		}[Picture.algorithmType]

# Creates an algorithm one object 
def create_algorithm_one_object_json(Picture, json):
	
	# create a new alg1 object, Default 50 radius circles
	try:
		newAlg1 = AlgorithmOne(
			picture = Picture,
			nearX = json['nearTargetX'], 
			nearY = json['nearTargetY'],				
			farX = json['farTargetX'],
			farY = json['farTargetY'],
			nearDistance = json['nearTargetEstimatedDistance'],
			farDistance = json['farTargetEstimatedDistance'],
			nearRadius =  50,
			farRadius = 50,
			)
		newAlg1.save()
	except Exception as e:
		print("Issue creating algorithm object")
		print (e)
		return False
	return True 

# Creates an algorithm one object 
def create_algorithm_one_object(Picture, form):
	
	# create a new alg1 object
	if form.is_valid():
		newAlg1 = AlgorithmOne(
			picture = Picture,
			nearX = form.cleaned_data.get('nearX'), 
			nearY = form.cleaned_data.get('nearY'),				
			farX = form.cleaned_data.get('farX'),
			farY = form.cleaned_data.get('farY'),
			nearDistance = form.cleaned_data.get('nearDistance'),
			farDistance = form.cleaned_data.get('farDistance'),
			nearRadius = form.cleaned_data.get('nearRadius'),
			farRadius = form.cleaned_data.get('farRadius'),
			)
		newAlg1.save()
		return True
	return False 

# Creates an algorithm Two object. 
def create_algorithm_two_object_json(json):
	return False 

# Creates an algorithm one object. File Data comes in the form 
# request.FILES
def create_algorithm_two_object(Picture, form, fileData):
	
	# Create a new alg1 object
	if form.is_valid():
		try:
			newAlg2 = AlgorithmTwo(
				picture = Picture,
				image2 = fileData['pic2'],
				nearX = form.cleaned_data.get('nearX'), 
				nearY = form.cleaned_data.get('nearY'),				
				farX = form.cleaned_data.get('farX'),
				farY = form.cleaned_data.get('farY'),
				nearDistance = form.cleaned_data.get('nearDistance'),
				farDistance = form.cleaned_data.get('farDistance'),
				nearRadius = form.cleaned_data.get('nearRadius'),
				farRadius = form.cleaned_data.get('farRadius'))
			newAlg2.save()
		except Exception as e:
			print(e)
			return False 

		return True
	return False 


# Edits an algorithm obe object based off given form data
def edit_algorithm_one_object(form, algorithmOneObject):
	
	if form.is_valid():
		algorithmOneObject.nearX = form.cleaned_data.get('nearX');
		algorithmOneObject.nearY = form.cleaned_data.get('nearY');
		algorithmOneObject.farX = form.cleaned_data.get('farX');
		algorithmOneObject.farY = form.cleaned_data.get('farY');
		algorithmOneObject.nearDistance = form.cleaned_data.get('nearDistance');
		algorithmOneObject.farDistance = form.cleaned_data.get('farDistance');
		algorithmOneObject.nearRadius = form.cleaned_data.get('nearRadius');
		algorithmOneObject.farRadius = form.cleaned_data.get('farRadius');
		algorithmOneObject.save();
		return True

	return False

# Edits an algorithm obe object based off given form data
def edit_algorithm_two_object(form, algorithmTwoObject, FileData):
	
	if form.is_valid():
		algorithmTwoObject.nearX = form.cleaned_data.get('nearX');
		algorithmTwoObject.nearY = form.cleaned_data.get('nearY');
		algorithmTwoObject.farX = form.cleaned_data.get('farX');
		algorithmTwoObject.farY = form.cleaned_data.get('farY');
		algorithmTwoObject.nearDistance = form.cleaned_data.get('nearDistance');
		algorithmTwoObject.farDistance = form.cleaned_data.get('farDistance');
		algorithmTwoObject.nearRadius = form.cleaned_data.get('nearRadius');
		algorithmTwoObject.farRadius = form.cleaned_data.get('farRadius');
		algorithmTwoObject.save();
		return True

	return False

# Creates an appropriate algorithm form object given a picture object and its form
def apply_create_form(Picture, form, Data = None):
	return { 
	'AlgorithmOne': create_algorithm_one_object(Picture, form), 
	'AlgorithmTwo': create_algorithm_two_object(Picture, form, Data)
	}[Picture.algorithmType]

# Edits an appropriate algorithm object based off given form
def apply_edit_form(form, algorithmObject, Data = None):
	return {
	"AlgorithmOne" : edit_algorithm_one_object(form, algorithmObject),
	"AlgorithmTwo" : edit_algorithm_two_object(form, algorithmObject, Data)
	}[algorithmObject.picture.algorithmType]

# Retreives the appropriate html page given a picture object
def retreive_html_page(Picture):
	return {
	"AlgorithmOne" : 'algorithm_one.html',
	"AlgorithmTwo" : 'algorithm_two.html'
	}[Picture.algorithmType]

# Edit an algorithm given a picture
def edit_algorithm(request, Picture, algorithmObject, html_page):
	file_data = None

	# POST Request
	if request.method == 'POST':

		# Is there file information in the request?
		if hasattr(request, 'FILES'):
			form = retreive_algorithm_form(Picture, request.POST, request.FILES)
			file_data = request.FILES
		else:
			form = retreive_algorithm_form(Picture, request.POST)

		success = apply_edit_form(form, algorithmObject, request.FILES)

		if success:
			return HttpResponseRedirect("/picture/view/" + str(Picture.id))
		else:
			return HttpResponse("Internal Server Error info: file_upload Line 182. Please contact administrator")
		return HttpResponse("Post request to edit algorithm")

	# GET Request
	else:
		form = retreive_algorithm_form(Picture) 
		return render_to_response(html_page, {'has_alg': True,'form': form, "picture" : Picture,  "algorithm": algorithmObject}, 
			context_instance=RequestContext(request))

# Apply de algorithm
# URL /picture/<picId>/
@login_required
def apply_algorithm(request, picId = -1):
	if request.user.is_certified is False:
		return render_to_response('not_certified.html')
	pic = Picture.objects.get(id = picId)
	alg = retreive_algorithm_object(pic)
	html_page = retreive_html_page(pic)
	file_data = None
	
	# If we already have a algorithm object associated with this picture,
	# We must edit the algorithm
	if len(alg) > 0:
		return edit_algorithm(request, pic, alg[0], html_page)

	if picId !=-1:
		# On POST
		if request.method == 'POST':

			# Is there file information in the request?
			if hasattr(request, 'FILES'):
				form = retreive_algorithm_form(pic, request.POST, request.FILES)
				file_data = request.FILES
			else: 
				form = retreive_algorithm_form(pic, request.POST)

			# Apply the creation form with the following variables
			if(debugging()):
				print("Our algorithm type at line 207 = ")
				print(pic.algorithmType)

			success = apply_create_form(pic, form, file_data)

			if success:
				return HttpResponseRedirect("/picture/view/" + picId)
			else: 
				return HttpResponse("Internal Server Error on file_upload.views in apply_algorithm")
				# TODO

		# On GET
		else:
			form = retreive_algorithm_form(pic)
			
		if(debugging()):
			print("This is the html page: " + html_page)
			print("This is the alg type: " + pic.algorithmType)

		return render_to_response(html_page, {'has_alg': False,'form': form, "picture" : pic }, 
			context_instance=RequestContext(request))

	# Invalid picture id	
	else: 
		return HttpResponseRedirect("/gallery")

# Convert integer to algorithm name
def int_to_algorithm(answer):
	return {
	'1':"AlgorithmOne",
	'2':"AlgorithmTwo"
	}[answer]

# index is responsible for the main upload page
# Url: /file_upload/
@login_required
def index(request):
	if request.user.is_certified is False:
		return render_to_response('not_certified.html')
	
	# If there is a picture to upload
	if request.method == 'POST':

		form = picture_upload_form(request.POST, request.FILES)
		
		# Create a new picture object
		if form.is_valid():
			newPic = Picture(
				image = request.FILES['pic'], 
				user=request.user, 
				eVisualRange=form.cleaned_data.get('estimatedVr'), 
				description=form.cleaned_data.get('description'),
				algorithmType=int_to_algorithm(form.cleaned_data.get('algorithmType'))
				)
			newPic.save()

			# Create new tag object
			t = form.cleaned_data['location']
			newTag = Tag(picture = newPic, text = t.lower())
			newTag.save()
			
			return HttpResponseRedirect("/picture/" + str(newPic.id));

	# If Get Request
	else:
		form = picture_upload_form()
	
	return render_to_response('file_upload_page.html', {'form': form}, context_instance=RequestContext(request))



# The upload url for the app
@csrf_exempt
def upload(request):
	if debugging():
		print("I am uploading!")

	if request.method == 'POST':
		response_data = {}
		created_algorithm_object = None
		newPic = None

		# S is our JSON object
		s = json.loads(request.body);

		# Verify user
		toke = AuthToken.objects.filter(token=s['secretKey'])
		if toke.count() > 0:
			AuthToken.objects.get(token=s['secretKey']).delete()
			image_data = b64decode(s['image'])
			userob = AirpactUser.objects.get(username=s['user'])
			
			# Default values
			_vrUnits = 'K'
			timeTaken = datetime.datetime.now()
			algType = ""
			desc = ""
			
			# Grab distance
			if 'distanceMetric' in s:
				if s['distanceMetric'] == 'miles':
					_vrUnits = 'M'
			
			# Grab time
			if 'time' in s:
				try:
					timeTaken = datetime.strptime(s['time'],"%Y.%m.%d.%H.%M.%S")
				except Exception as e:
					print(e.message)
			
			# Grab descripting
			if 'description' in s:
				if s['description'] is not None:
					desc = s['description']

			if debugging():
				print("About to create a picture object")
				print("Here is the JSON")

			# Create a picture object
			try:
				newPic = Picture(
								image = ContentFile(image_data), 
								description = desc, 
								algorithmType = int_to_algorithm(s['algorithmType']),
								user=userob, 
								eVisualRange=s['estimatedVisualRange'], 
								#geoX = float(s['gpsLatitude']),
								#geoY = float(s['gpsLongitude']),
								uploadTime = timeTaken,
								vrUnits = _vrUnits,
								)
				newPic.save()

				if debugging():
					print("Here is the newpic: ")
					print(newPic)

			except Exception as e:
				print("Issue creating image: ")
				print(e)
				newPic = None

			# Create the appropriate algorithm object
			try:
				if debugging():
					print("About to create an algorithm object")

				algorithmList = {"AlgorithmOne" : create_algorithm_one_object_json(newPic, s), 
								"AlgorithmTwo" : create_algorithm_two_object_json(s) }
				created_algorithm_object = algorithmList[int_to_algorithm(s['algorithmType'])]	

				if debugging():
					print("Created algorithm object: ")
					print(created_algorithm_object)

			except Exception as e:
				print(e.message)

			try:
				# Tags should be one location
				location = s['location']
				newTag = Tag(picture = newPic, text = location.lower())
				newTag.save()
			except Exception as e:
				print("Issue creating a location tag")
				print(e)

			response_data['status'] = 'success'
			
			if debugging():
				print("About to send response data")

			# Return the appropriate output information
			if created_algorithm_object is not None:
				try:
					response_data['output'] = retreive_algorithm_object(newPic).calculatedVisualRange
				except Exception as e:
					print("Error retreiving calculated visual range")
					print(e)
			else: 
				response_data['output'] = 0

			# Return the id of the new image, if possible
			if newPic is not None:
				response_data['imageID'] = newPic.id
			else: 
				response_data['imageID'] = -1

			if debugging():
				print("Sent response Data!")

			return HttpResponse(json.dumps(response_data), content_type="application/json")
		else:

			# The auth key failed
			response_data['status'] = 'keyFailed'
			return HttpResponse(json.dumps(response_data), content_type="application/json")
	else:

		# A horrid Get request was made
		return HttpResponse("For app uploads only")

@login_required
def delete_picture(request, id):
	if request.user.is_certified is False:
		return render_to_response('not_certified.html')
	img = Picture.objects.get(id = id)
	if request.user.id == img.user.id:
		img.delete()
	return edit_profile(request)


# View a specific picture from the gallery
# URL: /picture/view/<pic_id>/
def view_picture(request, picId = -1, comment_num=1):
	pictures = None
	computed_vr = 0
	if picId != -1:

		# POST response
		if request.method == 'POST':	
			return HttpResponseRedirect(reverse('file_upload.views.index'))

		# Good picture id
		p = Picture.objects.get(id = picId)

		# Tell the tag db to get alist of tags from the picture
		cur_tag = Tag.objects.filter(picture= p)

		# Find all images in given location
		location = cur_tag[0].text
		picture_tags = Tag.objects.filter(text=location).order_by("picture__uploadTime")
		pictures = []
		for picture_tag in picture_tags:
			pictures.append(picture_tag.picture)

		# Is there an algorithm associated with this picture
		alg = retreive_algorithm_object(p)
		if len(alg) > 0:
			computed_vr = alg[0].calculatedVisualRange

		this_comment_form = comment_form()

		# Setup range of image numbers for the 
		# Picture is the main picture, pictures is the side bitches. 
		return render_to_response( 'view_image.html', {'picture': p, 'computed_vr': computed_vr, 'pictures':pictures, 
			'tag':cur_tag[0], "comment_num": comment_num, 'comment_form': this_comment_form, }, 
			context_instance=RequestContext(request))

	# If we have an invalid picture id
	else:
		return HttpResponseRedirect("/gallery/")
		#redirect back to gallery

