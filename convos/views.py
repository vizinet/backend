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
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Standard import things
from django.shortcuts import render
from django.http import HttpResponse
from file_upload.models import Picture
from user_profile.models import AirpactUser
from convos.models import Comment
from convos.forms import comment_form
import datetime

# Function to View all the comments and post a comment
# URL /comments/<pic_id>/<page_num>
def comments(request, picId = -1, page = 99):
	comments_paginated = []
	if picId !=-1:
		p = Picture.objects.get(id = picId)
		if request.method == 'POST':	
			this_comment_form = comment_form(request.POST)
			try:
				if(this_comment_form.is_valid()):
					this_comment = Comment(
						picture = p,
						user = request.user,
						text = this_comment_form.cleaned_data.get('text'),
						submit_date = datetime.datetime.now()
					);
					this_comment.save();

				else:
					print("Comment form is not valid")
			except Exception as e:
				print(e)

		comments = Comment.objects.filter(picture = p).order_by("-submit_date")

		#Show 5 per page
		paginator = Paginator(comments, 5) 

		try:
			comments_paginated = paginator.page(page)
		except PageNotAnInteger:
			comments_paginated = paginator.page(1)
		except EmptyPage:
			comments_paginated = paginator.page(paginator.num_pages)
		except Exception as e:
			print(e)

		return render_to_response("comments.html",	
			{'comments': comments_paginated, "picture_id" : picId}, context_instance=RequestContext(request));

	# No picture present
	else:
		return HttpResponse("Sever Error occured")
	