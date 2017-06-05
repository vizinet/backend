# -*- coding: utf-8 -*-
"""
Copyright © 2017,
Laboratory for Atmospheric Research at Washington State University,
All rights reserved.

"""
from django.views.generic import ListView, DetailView
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect

# Standard import things
from django.shortcuts import render
from django.http import HttpResponse
from file_upload.models import picture
from user_profile.models import AirpactUser
from convos.models import Comment
from convos.forms import comment_form
import datetime

# Function to View all the comments and post a comment
def comments(request, picId = -1, page = 1):
	if picId !=-1:
		p = picture.objects.get(id = picId)
		if request.method == 'POST':	
			form = comment_form(request.POST)
			try:
				this_comment = Comment(
					picture = p,
					user = request.user,
					text = form.cleaned_data.get('text'),
					submit_date = datetime.datetime.now().replace(microsecond=0)
				);
				this_comment.save();
			except Exception as e:
				print(e)

		comments = Comment.objects.filter(picture = p)
		comments = reversed(comments)
		return render_to_response("comments.html", {'comments': comments}, context_instance=RequestContext(request));

	# No page present
	else:
		pass
	