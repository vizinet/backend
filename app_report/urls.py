# -*- coding: utf-8 -*-
"""
Copyright © 2017,
Laboratory for Atmospheric Research at Washington State University,
All rights reserved.
"""


from django.conf.urls import url

from . import views


email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

urlpatterns = [
    url(r'^send/$', views.send, name='send_report'),
]
