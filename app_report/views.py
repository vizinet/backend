# -*- coding: utf-8 -*-
"""
Copyright © 2017,
Laboratory for Atmospheric Research at Washington State University,
All rights reserved.
"""


import traceback
import json

from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.files.base import ContentFile
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail


# TODO: Write our notification system, classes and all.


developer_emails = ['lukedottec@gmail.com']
airpact_fire_email = 'airpactfire@gmail.com'


@csrf_exempt
def send(request):
    """Send app crash report to the specified email."""
    # TODO: Some authentication?
    if request.method != 'POST':
        return HttpResponse('This is a POST-only API.', status=404)
    try:
        # Grab email from JSON body.
        body_unicode = request.body.decode('utf-8')
	root = json.loads(body_unicode)
        indented_json_text = json.dumps(root, sort_keys=True, indent=4)
	username = root['CUSTOM_DATA'].get('username', None) 
	if username is not None:
	    subject = 'APP HAS CRASHED FOR %s' % username.upper()
	else:
	    subject = 'APP CRASH PRIOR TO LOGIN'
        send_mail('[AIRPACT-Fire][CrashReport] %s' % subject, indented_json_text, 
		  airpact_fire_email, developer_emails)
        return HttpResponse(status=204)
    except:
        return HttpResponse(traceback.format_exc(), status=404)
