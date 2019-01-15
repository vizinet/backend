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


@csrf_exempt
def send(request):
    """Send app crash report to the specified email."""
    # TODO: Some authentication?
    if request.method != 'POST':
        return HttpResponse('This is a POST-only API.', status=404)
    try:
        # Grab email from JSON body.
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        email = body['email'] 
	platform = body['platform']
	message = body.get('message', '')
        send_mail('[AIRPACT-Fire][{platform}] App has Crashed', message, \
		'airpactfire@gmail.com', [email])
        return HttpResponse(status=204)
    except:
        return HttpResponse(traceback.format_exc(), status=404)
