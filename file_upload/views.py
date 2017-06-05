# -*- coding: utf-8 -*-
"""
Copyright © 2017,
Laboratory for Atmospheric Research at Washington State University,
All rights reserved.

"""
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
import json
from time import time
from base64 import b64decode
from django.core.files.base import ContentFile
import datetime
from django.shortcuts import render
from django.http import HttpResponse
from file_upload.models import picture
from file_upload.models import tag
from user_profile.models import AuthToken
from user_profile.models import AirpactUser
from user_profile.views import edit_profile
from file_upload.forms import picture_upload_form
from file_upload.forms import picture_edit_form
from convos.forms import comment_form
from django.contrib.auth.decorators import login_required


# index is responsible for the main upload page
# Url: /file_upload
@login_required
def index(request):
	if request.user.is_certified is False:
		return render_to_response('not_certified.html')
	
	#if there is a picture to upload
	if request.method == 'POST':

		form = picture_upload_form(request.POST, request.FILES)

		# Create a new picture object
		if form.is_valid():
			newPic = picture(
				pic = request.FILES['pic'], 
				user=request.user, 
				vr=form.cleaned_data.get('vr'), 
				description=form.cleaned_data.get('description'),
				highX=form.cleaned_data.get('farX'), 
				highY=form.cleaned_data.get('farY'), 
				lowX=form.cleaned_data.get('nearX'), 
				lowY=form.cleaned_data.get('nearY'), 
				nearTargetDistance = form.cleaned_data.get('nearDistance'),
				farTargetDistance = form.cleaned_data.get('farDistance'),
				radiusHigh = form.cleaned_data.get('radiusFar'),
				radiusLow = form.cleaned_data.get('radiusNear'));
			newPic.save()
			
			t = form.cleaned_data['location']

			#20 dollars in my pocket
			newTag = tag(picture = newPic, text = t.lower())
			newTag.save()
			

			return HttpResponseRedirect(reverse('file_upload.views.index'))

	# If Get Request
	else:
		form = picture_upload_form()
	
	return render_to_response('file_upload_page.html',{'form': form}, context_instance=RequestContext(request))

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
				newPic = picture(pic = ContentFile(image_data,str(str(time())+".jpg")), 
								description = desc, 
								user=userob, 
								vr=s['visualRangeOne'], 
								highColor=int(s['highColor']),
								highX=float(s['highX']), 
								highY=float(s['highY']),
								lowColor=int(s['lowColor']),
								lowX=float(s['lowX']),
								lowY=float(s['lowY']),
								geoX = float(s['geoX']),
								geoY = float(s['geoY']),
								vrUnits = _vrUnits,
								uploaded = timeTaken,
								algorithmType = algType,
								farTargetDistance = float(s['visualRangeTwo']),
								nearTargetDistance = float(s['visualRangeOne'])
								 );
			except Exception as e:
				print(e.message)

			newPic.save()
			conversations = convoPage(picture = newPic)
			conversations.save()

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
	img = picture.objects.get(id = id)
	print("users id: "+str(request.user.id)+"pictureid:"+str(img.id))
	if request.user.id == img.user.id:
		print("deleteing shit")
		img.delete()
	return edit_profile(request)


# View a specific picture from the gallery
# URL: /picture/view/<pic_id>/
def view_picture(request, picId = -1, comment_num=1):
	pictures = None
	if picId != -1:

		# Good picture id
		p = picture.objects.get(id = picId)

		# Tell the tag db to get alist of tags from the picture
		cur_tag = tag.objects.filter(picture= p)

		# If the user wants to see more images:
		location = cur_tag[0].text
		picture_tags = tag.objects.filter(text=location).order_by("picture__uploaded")
		pictures = []
		for picture_tag in picture_tags:
			pictures.append(picture_tag.picture)

		# POST response
		if request.method == 'POST':
			
			picture_form = picture_edit_form(request.POST, request.FILES)
			if form.is_valid:

				# Updated the values
				edited_picture = picture.objects.get(id = picId)
				edited_picture.highX = form.cleaned_data.get('farX')
				edited_picture.highY = form.cleaned_data.get('farY')
				edited_picture.lowX =  form.cleaned_data.get('nearX')
				edited_picture.lowY =  form.cleaned_data.get('nearY')
				edited_picture.nearTargetDistance = form.cleaned_data.get('nearDistance')
				edited_picture.farTargetDistance = form.cleaned_data.get('farDistance')
				edited_picture.save()
				

			t = form.cleaned_data['location']

			# Generate the tags
			newTag = tag(picture = newPic, text = t.lower())
			newTag.save()
			

			return HttpResponseRedirect(reverse('file_upload.views.index'))

		# GET Response
		else:
			picture_form = picture_edit_form()

		this_comment_form = comment_form()

		print("comment_num: ")
		print(comment_num)
		# Setup range of image numbers for the 
		# Picture is the main picture, pictures is the side bitches. 
		return render_to_response( 'view_image.html', {'picture': p,'pictures':pictures, 
			'tag':cur_tag[0], "comment_num": comment_num, 'comment_form': this_comment_form, 
			'picture_form': picture_form }, context_instance=RequestContext(request))

	# If we have an invalid picture id
	else:
		return HttpResponseRedirect("/gallery")
		#redirect back to gallery

