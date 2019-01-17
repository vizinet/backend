# -*- coding: utf-8 -*-
"""
Copyright © 2017,
Laboratory for Atmospheric Research at Washington State University,
All rights reserved.
"""

"""AIRPACT_Fire URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from user_profile import views as user_view
from convos import views as convos_view
from file_upload import views as file_upload_views
from user_profile import views as user_profile_views
from app_report import views as app_report_views
from convos import views as comment_views
from django_comments.models import Comment
from . import views
from .views import LocationAutocomplete
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    url(r'^$', views.index, name="home"),
    url(r'^map/$', views.map, name="map"),
    url(r'^tag-autocomplete/$', LocationAutocomplete.as_view(), name='location-autocomplete'),
    url(r'^admin_page$', views.admin_page, name="adminPage"),
    url(r'^uncertified$', views.uncertified, name="uncertified"),
    url(r'^user/', include('user_profile.urls')),
    url(r'^gallery/$', views.gallery, name="gallery"),
    url(r'^gallery/(?P<page>\d+)/$', views.gallery, name='gallery'),
    url(r'^picture/view/(?P<picId>\d+)/$', file_upload_views.view_picture, name="view_picture"),
    url(r'^picture/(?P<picId>\d+)/$', file_upload_views.apply_algorithm, name="apply_algorithm"),
    url(r'^picture/location/(?P<picId>\d+)/$', file_upload_views.apply_location, name="apply_location"),
    url(r'^picture/edit/(?P<picId>\d+)/$', file_upload_views.edit_algorithm, name="edit_algorithm"),
    url(r'^picture/view/(?P<picId>\d+)/(?P<comment_num>\d+)/$', file_upload_views.view_picture, name="view_picture"),
    url(r'^file_upload/', include('file_upload.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^comments/(?P<picId>\d+)/$', comment_views.comments, name="comment_form_target"),
    url(r'^comments/(?P<picId>\d+)/(?P<page>\d+)/$', comment_views.comments, name="comment_form_target"),
    url(r'^downloads/', views.downloads, name="downloads"),
    url(r'^about/', views.about, name="about"),
    url(r'^index/', views.main, name="main"),
    url(r'^forum/user/register/', user_profile_views.register_user, name="forum_register"),
    url(r'^forum/user/resend-activation/', user_profile_views.register_user, name="forum_resend"),
    url(r'^forum/user/password-reset/', user_profile_views.forgot_password, name="forum_resend"),
    url(r'^forum/', include('spirit.urls'), name="forum"),
    url(r'^forum_notifications/', views.forum_notifications, name="forum_notifications"),
    url(r'^getPythonScripts/', views.getPythonScripts, name="getPythonScripts"),
    url(r'^report/', include('app_report.urls')),
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
