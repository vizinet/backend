# -*- coding: utf-8 -*-
"""
Copyright © 2017,
Laboratory for Atmospheric Research at Washington State University,
All rights reserved.

"""
# Django pre-built libraries 
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.core.context_processors import csrf
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt

# Custom Django
from file_upload.models import Picture, Tag, AlgorithmOne
from file_upload.forms import GallerySortForm
from django.contrib.auth.decorators import login_required
from user_profile.models import AirpactUser

# Other 
import json
import urllib
from datetime import datetime
from dal import autocomplete

# The Home Page
# URL: /
def index(request):
	newestPictures = Picture.objects.all().order_by("-uploadTime")[:20]
	return render_to_response('index2.html',{'newestPictures' : newestPictures}, context_instance=RequestContext(request))
	
def main(request):
	return render_to_response('welcome.html', context_instance=RequestContext(request))

def forum(request):
	return render_to_response('forum.html', context_instance=RequestContext(request))

@csrf_exempt
@login_required
def admin_page(request):
	if request.user.is_custom_admin is False:
		return HttpResponseRedirect('/')
	if request.user.is_certified is False:
		return render_to_response('not_certified.html')

	users = AirpactUser.objects.all()
	if(request.method == 'POST'):
		print(request.POST)
		username = request.POST.get("ourUser",False)
		user = AirpactUser.objects.get(username=username)
		the_type = request.POST['the_type']
		
		if(the_type == "certify"):
			user.is_certified = True 
			user.save()

		if(the_type == "uncertify"):
			user.is_certified = False 
			user.save()

		if(the_type == "make_admin"):
			user.is_custom_admin = True
			user.save() 

		if(the_type == "unmake_admin"):
			user.is_custom_admin = False
			user.save() 

		if(the_type == "delete"):
			user.delete()

	return render_to_response('custom_admin_page.html', {'users': users})

def uncertified(request):
	return render_to_response('not_certified.html')

def test(request):
	return render_to_response('hello.html', RequestContext(request))

#The autocomplete function for tabs
class LocationAutocomplete(autocomplete.Select2ListView):
    
    def get_list(self):
        qs = tag.objects.all()
        tag_names = []
        if self.q:
            qs = qs.filter(text__istartswith=self.q)

        for tagy in qs:
        	if (tagy.text) not in tag_names:
        		tag_names.append(tagy.text)

        return tag_names


#This is the gallery
# URL: /gallery/<page_num>
def gallery(request, page = 1):
	allpictures = Picture.objects.all().order_by("-uploadTime")
	alltags = Tag.objects.all()

	# Gallery search form 
	form = GallerySortForm();
	if request.method == 'POST':
		sortByList=[];

		form = GallerySortForm(request.POST)
		if form.is_valid():
			
			# Order by
			if form.cleaned_data.get("ascending") != "" and form.cleaned_data.get("ascending") != 0:
				allpictures = order_pictures(form.cleaned_data.get("ascending"), allpictures)

			# Find by vr
			if form.cleaned_data.get("visual_range")  != "" and form.cleaned_data.get("visual_range") != 0:
				allpictures = find_pictures_vr(form.cleaned_data.get("visual_range"), allpictures)
				print(form.cleaned_data.get("visual_range"))
				#page = 1

			# Find by date (beginning)
			if form.cleaned_data.get("date1") != "":
				d = datetime.strptime(form.cleaned_data.get("date1"),"%m/%d/%Y")
				allpictures = allpictures.filter(uploadTime__gte=d)
				#page = 1

			# Find by date (end)
			if form.cleaned_data.get("date2") != "":
				d = datetime.strptime(form.cleaned_data.get("date2"),"%m/%d/%Y")
				allpictures = allpictures.filter(uploadTime__lte=d)
				#page = 1

			# Find by location (must be last since function returns a list)
			if form.cleaned_data.get("location") != "":
				allpictures = find_pictures_tag(form.cleaned_data.get("location"), allpictures, alltags)
				#page = 1
	

	paginator = Paginator(allpictures, 12) #Show 12 per page
	try:
		pictures = paginator.page(page)
	except PageNotAnInteger:
		pictures = paginator.page(1)
	except EmptyPage:
		pictures = paginator.page(paginator.num_pages)

	return render_to_response('gallery.html', {'pictures': pictures, 'form': form}, context_instance=RequestContext(request))

# function to order the pictures based off the form value
def order_pictures(x, pictures):
	return {
	'0': pictures.order_by("uploadTime"),
	'1': pictures.order_by("-uploadTime"),
	'2': pictures.order_by("eVisualRange"),
	'3': pictures.order_by("-eVisualRange"),
	}[x]

# A switch statement for finding the pictures based on visual range
def find_pictures_vr(x, pictures):
	return {
		'0': pictures,
		'1': pictures.filter(eVisualRange__lte=10.0),
		'2': pictures.filter(eVisualRange__gte=10.0, eVisualRange__lte=30.0 ),
		'3': pictures.filter(eVisualRange__gte=30.0, eVisualRange__lte=100.0 ),
		'4': pictures.filter(eVisualRange__gte=100.0, eVisualRange__lte=500.0 ),
		'5': pictures.filter(eVisualRange__gte=500.0),
	}[x]

#Find pictures by tag, warning, returns a list of pictures
#as opposed to a picture object
def find_pictures_tag(location, pictures, alltags):
	
	foundpictures = []
	checkpictures = []
	alltags = alltags.filter(text__startswith=location)

	# Convert pictures into a list
	for picture in pictures:
		for tag in alltags:
			if(tag.picture == picture):
				foundpictures.append(picture)

	return foundpictures

def downloads(request):
	return render_to_response("downloads.html", context_instance=RequestContext(request))

def about(request):
	newestPictures = Picture.objects.all().order_by("-uploadTime")[:4]
	return render_to_response("about.html", {'newestPictures' : newestPictures}, context_instance=RequestContext(request))
	
@csrf_exempt
def getPythonScripts(request):
	opener = urllib.URLopener()
	script1URL = "https://s3-us-west-2.amazonaws.com/airpactfire/static/media/scripts/alg1.py"
	script2URL = "https://s3-us-west-2.amazonaws.com/airpactfire/static/media/scripts/alg2.py"
	responseData = {}
	script1File = opener.open(script1URL)
	script2File = opener.open(script2URL)
	responseData['alg1'] = script1File.read()
	responseData['alg2'] = script2File.read()
	return HttpResponse(json.dumps(responseData), content_type="application/json")




