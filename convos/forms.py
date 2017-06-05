# -*- coding: utf-8 -*-
"""
Copyright © 2017,
Laboratory for Atmospheric Research at Washington State University,
All rights reserved.

"""
from django import forms
from convos.models import Comment

class comment_form(forms.Form):
	text = forms.CharField(label = "Add comment")