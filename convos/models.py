# -*- coding: utf-8 -*-
"""
Copyright © 2017,
Laboratory for Atmospheric Research at Washington State University,
All rights reserved.

"""
from __future__ import unicode_literals
from django.db import models
from file_upload.models import Picture
from user_profile.models import AirpactUser

# Comment Class


class Comment(models.Model):
    picture = models.ForeignKey(Picture, default=-1, on_delete=models.CASCADE)
    user = models.ForeignKey(AirpactUser, default=-1)
    text = models.TextField(default="", blank=True)
    submit_date = models.TextField(default="", blank=True)

    def __str__(self):
        return self.text
