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
from file_upload.models import Picture, Tag, AlgorithmOne
from user_profile.models import AuthToken, AirpactUser
from user_profile.views import edit_profile
from file_upload.forms import picture_upload_form, algorithm_one_form
from convos.forms import comment_form

# Other
from base64 import b64decode
from time import time
import datetime
import json

# Are we debuggin?
def debugging():
	return True

# Queries algorithms given a picture id, returns all appropriate algorithms
def retreive_algorithm_object(Picture):
	return {
	"AlgorithmOne" : AlgorithmOne.objects.filter(picture = Picture),
	"AlgorithmTwo" : None
	}[Picture.algorithmType]

# Retreives a form given a picture Django object
def retreive_form(Picture, postData = None):
	if postData is None:
		return {
		"AlgorithmOne" : algorithm_one_form(),
		"AlgorithmTwo" : None
		}[Picture.algorithmType]
	else:
		return {
		"AlgorithmOne" : algorithm_one_form(postData),
		"AlgorithmTwo" : None
		}[Picture.algorithmType]

# Creates an algorithm one object given a picture object and a completed
# form. Returns True on success
def create_algorithm_one_object(picture, form):
	# create a new alg1 object
	try:
		newAlg1 = AlgorithmOne(
			picture = newPic,
			nearX=float(form['nearX']), 
			nearY=float(form['nearY']),				
			farX=float(form['farX']),
			farY=float(form['farY']),
			nearDistance = float(form['nearDistance']),
			farDistance = float(form['farDistance'])
			)
		newAlg1.save()
	except Exception as e:
		print(e)
		return False

	return True

# Creates an appropriate algorithm object given a picture object and its form
# Url: /picture/pic_id
def apply_form(picture, form):
	return {
	"AlgorithmOne" : create_algorithm_one_object(picture, form),
	"AlgorithmTwo" : None
	}[Picture.algorithmType]

# Retreives the appropriate html page given a picture object
def retreive_html_page(Picture):
	return {
	"AlgorithmOne" : 'algorithm_one.html',
	"AlgorithmTwo" : None
	}[Picture.algorithmType]

# Edit an algorithm given a picture
def edit_algorithm(request, algorithm_object):
	
	if request.method == 'POST':
		return HttpResponse("Post request to edit algorithm")
	else: 
		return HttpResponse("Post request to edit algorithm")

# Apply de algorithm
def apply_algorithm(request, picId = -1):
	pic = Picture.objects.get(id = picId)
	alg = retreive_algorithm_object(pic)
	
	# If we already have a algorithm object associated with this picture,
	# We must edit the algorithm
	if len(alg) > 0:
		return edit_algorithm(request, alg)

	if picId !=-1:
		# On POST
		if request.method == 'POST':
			form = retreive_form(pic, request.POST)
			success = apply_form(form)
			if success:
				return HttpResponseRedirect("/picture/view/" + newPic.id)
			else: 
				return HttpResponse("Internal Server Error on file_upload.views in apply_algorithm")
				# TODO

		# On GET
		else:
			form = retreive_form(pic)
			html_page = retreive_html_page(pic)

		if(debugging()):
			print("This is the html page: " + html_page)
			print("This is the alg type: " + pic.algorithmType)
			print("This is the form: " )


		return render_to_response(html_page, {'has_alg': False,'form': form, "picture" : pic }, context_instance=RequestContext(request))

	# Invalid picture id	
	else: 
		return HttpResponseRedirect("/gallery")

# Convert integer to algorithm name
def int_to_algorithm(answer):
	return {
	'0':"AlgorithmOne",
	'1':"TODO"
	}[answer]

# index is responsible for the main upload page
# Url: /file_upload/
@login_required
def index(request):
	#if request.user.is_certified is False:
		#return render_to_response('not_certified.html')
	
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
	if request.method == 'POST':
		response_data = {}

		# S is our JSON object
		s = json.loads(request.body);

		toke = AuthToken.objects.filter(token=s['secretKey'])
		if toke.count() > 0:
			AuthToken.objects.get(token=s['secretKey']).delete()
			image_data = b64decode(s['image'])
			userob = AirpactUser.objects.get(username=s['user'])
			
			_vrUnits = 'K'
			timeTaken = datetime.now()
			algType = ""
			desc = " "
			
			try:
				for key, value in s.iteritems():
					if key != 'image' or key == 'description' and s['descrption'] is not None:
						print(key +":" + str(value))

			except Exception as e:
				print("ERROR ITERATING KESY: "+e.message +"NOT FOUND")
			if "highColor" in s:
				print("FOUND HIGH COLOR it's:" + s["highColor"])

			if 'distanceUnits' in s:
				if s['distanceUnits'] == 'miles':
					_vrUnits = 'M'
			
			if 'time' in s:
				try:
					timeTaken = datetime.strptime(s['time'],"%Y.%m.%d.%H.%M.%S")
				except Exception as e:
					print(e.message)

			if 'algorithmType' in s:
				algType = s['algorithmType']
			
			if 'description' in s:
				if s['description'] is not None:
					desc = s['description']

			try:
				newPic = picture(
								image = ContentFile(image_data,str(str(time())+".jpg")), 
								description = desc, 
								user=userob, 
								eVisualRange=s['visualRangeOne'], 
								geoX = float(s['geoX']),
								geoY = float(s['geoY']),
								uploadTime = timeTaken,
								vrUnits = _vrUnits,
								)

				newPic.save()	
				algorithmOne = AlgorithmOne(
								picture = newPic,
								highX=float(s['highX']), 
								highY=float(s['highY']),
								lowColor=int(s['lowColor']),
								lowX=float(s['lowX']),
								lowY=float(s['lowY']),
								farTargetDistance = float(s['visualRangeTwo']),
								nearTargetDistance = float(s['visualRangeOne'])
					)

			except Exception as e:
				print(e.message)


			#Creating some conversation stuffs
			print(s['tags'])
			tags = s['tags'].split(",")
			for t in tags:
				newTag = tag(picture = newPic, text = t.lower())
				newTag.save()

			response_data['status'] = 'success'
			response_data['TwoTargetContrastOutput'] = newPic.twoTargetContrastVr
			response_data['imageID'] = newPic.id
			return HttpResponse(json.dumps(response_data), content_type="application/json")
		else:
			response_data['status'] = 'keyFailed'
			return HttpResponse(json.dumps(response_data), content_type="application/json")
	else:
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
		return HttpResponseRedirect("/gallery")
		#redirect back to gallery

